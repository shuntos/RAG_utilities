FRESH GARDEN FRUIT SHOP — 2025 RAG TUTORIAL DATASET

Entirely synthetic dataset for demonstrations, not real business or health data.

FILES
products.csv: products, origins, retail prices, reorder levels
nutrition.csv: approximate nutrients and fictional demo nutrition score
suppliers.csv: supplier directory with invalid example domains
staff.csv: fictional staff
staff_shifts_2025.csv: dated staff shifts
sales_2025.csv: daily per-product sales records
deliveries_2025.csv: dated stock receipts
waste_2025.csv: dated spoilage/discards in units
inventory_daily_2025.csv: daily opening, received, sold, wasted and closing stock
expenses_2025.csv: simulated labor and overhead allocations
daily_summary_2025.csv: daily store totals
shop_handbook.txt: narrative policy document for chunking
customer_faq.txt: narrative FAQs for chunking
rag_chunks.jsonl: pre-chunked narrative and catalog records

DEMO RAG RECOMMENDATION
Chunk the TXT documents and embed the chunks with nomic-embed-text. Embed product descriptions to find products semantically. For exact numbers and arithmetic, use SQL/pandas queries against CSVs rather than embedding every changing numeric row. Combine retrieved text and queried facts in the LLM prompt.

IMPORTANT
The last available inventory date is 2025-12-31, not today. Never describe it as live stock. Units are items/packs, not kilograms. Sales are aggregated by product per day, not individual customer receipts.
