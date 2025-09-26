import io
import pandas as pd
from django.db import transaction
from .models import Product

# توجه: pandas از file-like object پشتیبانی می‌کنه
def import_products_from_file(file_obj):
    """
    file_obj: UploadedFile (InMemoryUploadedFile or TemporaryUploadedFile)
    بازمی‌گرداند: {'created': int, 'updated': int, 'skipped': int, 'errors': [..]}
    """
    created = 0
    updated = 0
    skipped = 0
    errors = []

    try:
        # خواندن با pandas (پشتیبانی از xls/xlsx)
        # اگر با ارور مواجه شد، ممکنه لازم باشه explicit engine بدیم:
        # df = pd.read_excel(file_obj, engine='xlrd')  # برای xls
        # df = pd.read_excel(file_obj, engine='openpyxl')  # برای xlsx
        # pandas خودش اغلب engine مناسب رو انتخاب می‌کنه
        df = pd.read_excel(file_obj)
    except Exception as e:
        errors.append(str(e))
        return {'created': created, 'updated': updated, 'skipped': skipped, 'errors': errors}

    # ---- mapping ستون‌ها ----
    # تلاش برای پیدا کردن نام ستون‌های معمول؛ اگر پروژه شما ستون‌های متفاوتی داره،
    # اینجا مطابق فایل اکسل‌تون نام ستون‌ها رو اصلاح کن.
    col_map = {
        'serial': None,
        'name': None,
        'description': None,
        'price': None,
        'stock': None
    }

    # lowercase column names for flexible mapping
    df_columns = {c.lower(): c for c in df.columns}

    # جستجوی ستون‌های معقول
    for key in col_map.keys():
        # mapping rules (می‌تونی گسترشش بدی)
        candidates = {
            'serial': ['serial', 'sku', 'کد', 'سریال', 'کد کالا', 'code'],
            'name': ['name', 'product', 'title', 'نام', 'نام کالا'],
            'description': ['description', 'desc', 'توضیحات'],
            'price': ['price', 'قیمت', 'price_toman', 'cost'],
            'stock': ['stock', 'qty', 'quantity', 'موجودی', 'تعداد']
        }
        for cand in candidates.get(key, []):
            if cand.lower() in df_columns:
                col_map[key] = df_columns[cand.lower()]
                break

    # اگر ستون serial پیدا نشد → خطا (ما باید بر اساس سریال عمل کنیم)
    if not col_map['serial']:
        errors.append("ستون سریال/sku در فایل پیدا نشد. نام ستون را بررسی کنید.")
        return {'created': created, 'updated': updated, 'skipped': skipped, 'errors': errors}

    # پردازش هر ردیف
    for idx, row in df.iterrows():
        try:
            serial = str(row[col_map['serial']]).strip()
            if serial in ('nan', '', 'None', None):
                skipped += 1
                continue

            name = row[col_map['name']] if col_map['name'] else ''
            description = row[col_map['description']] if col_map['description'] else ''
            price = row[col_map['price']] if col_map['price'] else 0
            stock = row[col_map['stock']] if col_map['stock'] else 0

            # تبدیل مقادیری که ممکنه نان باشند
            try:
                price = float(price) if pd.notna(price) else 0
            except:
                price = 0
            try:
                stock = int(stock) if pd.notna(stock) else 0
            except:
                try:
                    stock = int(float(stock))
                except:
                    stock = 0

            # update_or_create درون تراکنش
            with transaction.atomic():
                obj, created_flag = Product.objects.update_or_create(
                    serial=serial,
                    defaults={
                        'name': name,
                        'description': description,
                        'price': price,
                        'stock': stock
                    }
                )
                if created_flag:
                    created += 1
                else:
                    updated += 1

        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")
            skipped += 1
            continue

    return {'created': created, 'updated': updated, 'skipped': skipped, 'errors': errors}
