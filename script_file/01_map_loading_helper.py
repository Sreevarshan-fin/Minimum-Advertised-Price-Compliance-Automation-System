import glob
import os
import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse
import logging
from datetime import datetime

# ========================================================================================================================
#                                         🔴 Loading Seller Data code 🔴
# =======================================================================================================================


# =========================================================
# 1️⃣ CONFIG
# =========================================================

password = urllib.parse.quote_plus("@Sree05092001varshan")

engine = create_engine(
    f"mysql+pymysql://root:{password}@localhost:3306/map_db",
 echo=False)



SELLER_FOLDER = r"D:\AI_Course_2\#1_Data science\#7_MAP_Compliance_project\loading_seller_data\Seller Data"

USD_TO_INR = 90
AED_TO_INR = 25
GBP_TO_INR = 105


# =========================================================
# 2️⃣ ENSURE LOG TABLE
# =========================================================
def ensure_log_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS file_process_log (
                file_name VARCHAR(255) PRIMARY KEY,
                processed_ts DATETIME
            )
        """))
    print("✅ Log table ready")


# =========================================================
# 3️⃣ REMOVE DUPLICATE COLUMNS
# =========================================================
def remove_duplicate_columns(df):
    return df.loc[:, ~df.columns.duplicated()]


# =========================================================
# 4️⃣ SMART FILE READER
# =========================================================
def read_file_smart(path):
    if path.lower().endswith(".csv"):
        df = pd.read_csv(path)
    elif path.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(path)
    else:
        raise ValueError("Unsupported file format")

    print("   👉 Rows read:", len(df))
    print("   👉 Raw columns:", df.columns.tolist())
    return df


# =========================================================
# 5️⃣ CURRENCY CONVERSION
# =========================================================
def convert_to_inr(df):
    df.columns = df.columns.str.strip().str.lower()

    if "advertised_price_unconverted" in df.columns:
        df.rename(columns={"advertised_price_unconverted": "adv_price"}, inplace=True)

    required_cols = {"region", "adv_price"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["region"] = df["region"].astype(str).str.strip().str.upper()
    df["adv_price"] = pd.to_numeric(df["adv_price"], errors="coerce")

    print("   👉 Unique regions:", df["region"].unique())

    df["advertised_price_inr"] = df["adv_price"]

    # USD countries
    usd_regions = ["USD", "USA", "US", "CAN"]
    df.loc[df["region"].isin(usd_regions), "advertised_price_inr"] = (
            df.loc[df["region"].isin(usd_regions), "adv_price"] * USD_TO_INR
    )

    # AED countries
    aed_regions = ["AED", "UAE"]
    df.loc[df["region"].isin(aed_regions), "advertised_price_inr"] = (
            df.loc[df["region"].isin(aed_regions), "adv_price"] * AED_TO_INR
    )

    # GBP countries
    gbp_regions = ["UK", "GB", "GBP"]
    df.loc[df["region"].isin(gbp_regions), "advertised_price_inr"] = (
            df.loc[df["region"].isin(gbp_regions), "adv_price"] * GBP_TO_INR
    )

    df["adv_price"] = df["advertised_price_inr"]

    return remove_duplicate_columns(df)


# =========================================================
# 6️⃣ ALIGN TO SQL TABLE
# =========================================================
def align_to_seller_table(df):
    df.columns = df.columns.str.strip().str.lower()

    rename_map = {
        "adv_price": "advertised_price_unconverted",
        "advertised_price_inr": "advertised_price_unconverted",
        "seller data": "seller_datacol",
        "seller_data": "seller_datacol"
    }

    df = df.rename(columns=rename_map)
    df = remove_duplicate_columns(df)

    required_cols = [
        "sku",
        "marketplace",
        "seller_name",
        "region",
        "advertised_price_unconverted",
        "screenshot",
        "live_link",
        "seller_datacol"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df = df[required_cols]

    print("   👉 Final columns:", df.columns.tolist())
    return df


# =========================================================
# 7️⃣ LOAD ONLY NEW FILES
# =========================================================

'''
When a seller data file (Excel or CSV) is placed in the folder path, it should automatically load into SQL.

If a file has already been loaded into SQL and still exists in the folder, it must not be reloaded again. Only new files should be processed.

To achieve this, create a database table called file_process_log that stores the file name and processed datetime.
Before loading any file:

If the file name already exists in file_process_log, skip the file (do not load again).

If the file name does not exist in file_process_log, 
load the file into SQL and then insert its name and datetime into the log table.

This ensures that each file is processed only once in seller database.
'''


def load_new_price_files():
    print("🔍 Checking for new seller files...")

    ensure_log_table()

    #  DEBUG: folder check
    print("   👉 Folder exists:", os.path.exists(SELLER_FOLDER))
    logging.info("Checking for new seller files...")

    all_files = (
            glob.glob(os.path.join(SELLER_FOLDER, "*.csv")) +
            glob.glob(os.path.join(SELLER_FOLDER, "*.xlsx")) +
            glob.glob(os.path.join(SELLER_FOLDER, "*.xls"))
    )

    print(f"📁 Files found in folder: {len(all_files)}")
    print("   👉 All files:", [os.path.basename(f) for f in all_files])

    # processed files

    '''
    If the file name already exists in file_process_log, skip the file (do not load again).

    If the file name does not exist in file_process_log, 
    load the file into SQL and then insert its name and datetime into the log table.

    '''
    with engine.connect() as conn:
        try:
            processed_files = pd.read_sql(
                "SELECT file_name FROM file_process_log",
                conn
            )["file_name"].tolist()
        except Exception:
            processed_files = []

    print("   👉 Processed files:", processed_files)
    logging.info(f"Processing file: {processed_files}")

    new_files = [
        f for f in all_files
        if os.path.basename(f) not in processed_files
    ]

    print("   👉 New files:", [os.path.basename(f) for f in new_files])

    if not new_files:
        print("✅ No new files found")
        return False

    print(f"🚀 New files to process: {len(new_files)}")

    # process
    for file in new_files:
        fname = os.path.basename(file)
        print(f"\n⬇️ Processing: {fname}")

        try:
            df = read_file_smart(file)

            if df.empty:
                raise ValueError("File is empty")

            df = df.drop_duplicates()
            df = convert_to_inr(df)
            df = align_to_seller_table(df)

            print("   👉 Inserting into seller_data...")

            df.to_sql(
                "seller_data",
                engine,
                if_exists="append",
                index=False,
                method="multi"
            )

            print("   ✅ Inserted rows:", len(df))
            logging.info(f"Inserted rows: {len(df)}")

            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO file_process_log (file_name, processed_ts)
                    VALUES (:fname, NOW())
                """), {"fname": fname})

            print("   📝 File logged")

        except Exception as e:
            print(f"   ❌ FAILED: {fname}")
            print(f"   ❌ Reason: {e}")
            raise
            logging.error(f"FAILED file: {fname} | Reason: {e}")

    print("\n🎉 Process completed")
    return True


# ======================================================================================================================
#                          🔴 Price Monitoring Table Loading (Idempotent Incremental Logic) 🔴
# ======================================================================================================================
"""
❓Note : This is the Code where i faced the challenges.

PIPELINE ROLE
-------------
Builds the price_monitoring fact table using newly ingested seller observations.

WHY THIS STEP EXISTS
--------------------
Seller data arrives incrementally via files. This step:

• enriches seller observations with product + promo data  
• computes MAP violation status  
• ensures no historical duplication  
• supports safe re-runs (idempotent design)

CRITICAL GUARANTEES
-------------------
- Each seller row is processed exactly once  
- Pipeline can be rerun safely  
- No row explosion from promotional joins  
- Business logic applied consistently
"""


def append_price_monitoring(batch_id):
    # -------------------------------------------------------------------------------------------------
    # IMPORTANT: We DO NOT truncate price_monitoring (before i was using truncate but the problem historical loaded multiple times same data which processed before)
    # Reason:
    #   • Business requires historical accumulation
    #   • We rely on processed_flag for incremental control
    #   • Makes pipeline idempotent and restart-safe
    # -------------------------------------------------------------------------------------------------

    insert_sql = """
    INSERT INTO price_monitoring (
        sku,
        product_line,
        category,
        sub_category,
        seller_name,
        homologated_sellers,
        region,
        promo_PL,
        promo_sku,
        season,
        MAP,
        LLP,
        promotional_value,
        Promotional_price,
        advertised_price,
        violation_flag,
        violation_date,
        marketplace,
        batch_id
    )
    SELECT 
        -- ---------------------------------------------------------------------------------------------
        -- Product master attributes (dimension enrichment)
        -- ---------------------------------------------------------------------------------------------
        p.sku,
        p.product_line,
        p.category,
        p.sub_category,

        -- ---------------------------------------------------------------------------------------------
        -- Seller observation details (grain of the fact table)
        -- NOTE: seller_data is the TRUE driving table logically
        -- ---------------------------------------------------------------------------------------------
        se.seller_name,
        sm.homologated_sellers,
        se.region,

        -- ---------------------------------------------------------------------------------------------
        -- Promotional enrichment (latest season only)
        -- Prevents duplicate rows caused by multi-season promos
        -- ---------------------------------------------------------------------------------------------
        pa.pl,
        pa.sku AS promo_sku,
        pa.season,

        -- Pricing benchmarks
        p.MAP,
        p.LLP,
        pa.promotional_value,

        -- ---------------------------------------------------------------------------------------------
        -- Derived promotional price
        -- Business rule: promo reduces MAP when available
        -- ---------------------------------------------------------------------------------------------
        CASE
            WHEN pa.promotional_value IS NOT NULL
            THEN (p.MAP - pa.promotional_value)
            ELSE NULL
        END AS Promotional_price,

        -- Seller observed price
        se.advertised_price_unconverted,

        -- ---------------------------------------------------------------------------------------------
        -- MAP VIOLATION ENGINE (core business logic)
        -- Order of rules is CRITICAL
        -- ---------------------------------------------------------------------------------------------
        CASE
            -- No price shown by seller
            WHEN se.advertised_price_unconverted IS NULL 
                THEN 'PRICE has not displayed'

            -- Promotional violation check (highest priority)
            WHEN pa.promotional_value IS NOT NULL
                 AND se.advertised_price_unconverted < (p.MAP - pa.promotional_value)
                THEN 'VIOLATION'

            -- LLP fallback rule
            WHEN pa.promotional_value IS NULL
                 AND se.advertised_price_unconverted < p.LLP
                THEN 'VIOLATION'

            -- Otherwise compliant
            ELSE 'No Violation'
        END AS violation_flag,

        NOW(),                     -- processing timestamp
        se.marketplace,
        :batch_id                 -- batch lineage tracking

    FROM price_list_table p

    -- -------------------------------------------------------------------------------------------------
    -- 🔴 INCREMENTAL FILTER (MOST IMPORTANT LINE IN PIPELINE)
    -- Only process seller rows that have NOT been processed before.
    -- This is what makes the pipeline idempotent.
    -- -------------------------------------------------------------------------------------------------
    LEFT JOIN seller_data se
      ON se.sku = p.sku
     AND se.processed_flag = 0

    -- -------------------------------------------------------------------------------------------------
    -- Latest promotional record per SKU
    -- Prevents 1-to-many explosion from promo history.
    -- -------------------------------------------------------------------------------------------------
    LEFT JOIN (
        SELECT pa1.*
        FROM promotional_table pa1
        LEFT JOIN (
            SELECT sku, MAX(season) AS max_season
            FROM promotional_table
            GROUP BY sku
        ) latest
          ON pa1.sku = latest.sku
         AND pa1.season = latest.max_season
    ) pa ON p.sku = pa.sku

    -- Seller authorization mapping
    LEFT JOIN seller_mapping_table sm
      ON sm.sellers_name = se.seller_name
    """

    # -------------------------------------------------------------------------------------------------
    # TRANSACTION BLOCK
    # Guarantees atomicity:
    #   • either insert + update both succeed
    #   • or both rollback
    # -------------------------------------------------------------------------------------------------
    with engine.begin() as conn:
        # Insert monitoring rows for NEW seller observations only
        conn.execute(text(insert_sql), {"batch_id": batch_id})

        # -------------------------------------------------------------------------------------------------
        # 🔴 CRITICAL STATE TRANSITION
        # Mark processed seller rows to prevent reprocessing on next run.
        # This is the heart of incremental control.
        # -------------------------------------------------------------------------------------------------
        conn.execute(text("""
            UPDATE seller_data
            SET processed_flag = 1
            WHERE processed_flag = 0
        """))

    print("✅ price_monitoring appended")


# ======================================================================================================================
#                                              🔴Violation Table Creation🔴
# ======================================================================================================================
# 1. Violation Sending to all Seller each SKU
# 2. Violation if more than 3 suspending the Particular Category.

def append_violations_table():
    # STEP 1 — insert only violations
    insert_sql = """
    INSERT INTO violation_table (
        sku,
        seller_name,
        homologated_sellers,
        region,
        advertised_price,
        LLP,
        promotional_price,
        season,
        violation_flag,
        violation_date,
        marketplace        
    )
    SELECT
        sku,
        seller_name,
        homologated_sellers,
        region,
        advertised_price,
        LLP,
        Promotional_price,
        season,
        violation_flag,
        violation_date,
        marketplace

    FROM price_monitoring
    WHERE violation_flag = 'VIOLATION'
    """

    with engine.begin() as conn:
        conn.execute(text(insert_sql))

    print("✅ violations_table rebuilt successfully")


# ======================================================================================================================
#                                              🔴Letter Generation Code 🔴
# ======================================================================================================================

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

LETTER_FOLDER = "D:/MAP_letters"
os.makedirs(LETTER_FOLDER, exist_ok=True)

import re

def clean_filename(text):
    if text is None:
        return "UNKNOWN"
    return re.sub(r'[\\/*?:"<>|]', "", str(text)).strip()

def create_violation_letter(row):
    styles = getSampleStyleSheet()

    seller_name = clean_filename(row['seller_name'])
    sku = clean_filename(row['sku'])
    violation_id = row['violation_id']

    file_name = f"Violation_{violation_id}_{sku}_{seller_name}.pdf"
    output_path = os.path.join(LETTER_FOLDER, file_name)

    story = []

    story.append(Paragraph("<b>MAP Violation Notice</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    body = f"""
    Dear {row['seller_name']},<br/><br/>
    A MAP violation has been detected.<br/><br/>

    <b>Violation ID:</b> {row['violation_id']}<br/>
    <b>Details:</b><br/>
    SKU: {row['sku']}<br/>
    Advertised Price: {row['advertised_price']}<br/>
    LLP: {row['LLP']}<br/>
    Marketplace: {row['marketplace']}<br/><br/>

    Please take corrective action.<br/><br/>
    Regards,<br/>
    MAP Compliance Team
    """

    story.append(Paragraph(body, styles["Normal"]))

    doc = SimpleDocTemplate(output_path)
    doc.build(story)

    return output_path


def generate_letters():
    logging.info("Checking for new violations for letter generation...")

    # ⭐ ONLY fetch violations never sent before
    query = """
    SELECT v.*
    FROM violation_table v
    LEFT JOIN letter_history h
    ON v.violation_id = h.violation_id
    WHERE h.violation_id IS NULL
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        logging.info("No new letters required")
        return

    logging.info(f"Letters to generate: {len(df)}")

    for _, row in df.iterrows():
        try:
            # create PDF
            path = create_violation_letter(row)
            logging.info(f"Letter created: {path}")

            # store memory in history table
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO letter_history (
                        violation_id,
                        sku,
                        seller_name,
                        marketplace,
                        violation_date,
                        sent_ts
                    )
                    VALUES (:vid, :sku, :seller, :market, :vdate, NOW())
                """), {
                    "vid": row["violation_id"],
                    "sku": row["sku"],
                    "seller": row["seller_name"],
                    "market": row["marketplace"],
                    "vdate": row["violation_date"].date()
                })

        except Exception as e:
            logging.error(f"Letter failed for {row['seller_name']}: {e}")


# =========================================================
# 8️⃣ MAIN
# =========================================================
if __name__ == "__main__":
    new_data = load_new_price_files()

    if new_data:
        batch_id = datetime.now().strftime("%Y%m%d%H%M%S")
        append_price_monitoring(batch_id)
        append_violations_table()
        generate_letters()
    else:
        print("🟡 No new seller data — skipping price monitoring")


