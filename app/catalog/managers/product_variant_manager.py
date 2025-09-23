from common.models import SystemSettings


class ProductVariantManager:
    def __init__(self):
        pass
    
    @staticmethod
    def generate_sku_code():
        settings = SystemSettings.objects.filter(
            name='LAST_SKU_CODE_VALUE').first()
        last_sku_value = settings.value
        current_sku = int(last_sku_value) + 1
        settings.value = str(current_sku)
        settings.save()
        
        return f"SKU{str(current_sku).zfill(8)}"
    

        