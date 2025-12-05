from catalog.bulk_upload_scripts.base import BulkUploadeBaseClass
from catalog.models import Product, Collection, Category, Occasion, Tag, ProductImage
from common.miscellaneous_values.aws_buckets import AWSBuckets
from catalog.miscellaneous_values.product_image import ImageDimensions
from catalog.handlers.image_upload import run_pipeline


class BULK_UPLOAD_PRODUCTS(BulkUploadeBaseClass):
    required_headers = ["name", "description", "color", "collection_ids", "image1"]
    optional_headers = ["fabric", "category_ids", "occasion_ids", "tag_ids", "image2", "image3", "image4", "image5", "url_slug"]

    def validate_collection_ids(self, collection_ids: list):
        valid_ids = []
        for cid in collection_ids:
            cid = cid.strip()
            if cid.isdigit() and Collection.objects.filter(id=int(cid)).exists():
                valid_ids.append(int(cid))
        return valid_ids
    
    def validate_category_ids(self, category_ids: list):
        valid_ids = []
        for cid in category_ids:
            cid = cid.strip()
            if cid.isdigit() and Category.objects.filter(id=int(cid)).exists():
                valid_ids.append(int(cid))
        return valid_ids
    
    def validate_occasion_ids(self, occasion_ids: list):
        valid_ids = []
        for oid in occasion_ids:
            oid = oid.strip()
            if oid.isdigit() and Occasion.objects.filter(id=int(oid)).exists():
                valid_ids.append(int(oid))
        return valid_ids
    
    def validate_tag_ids(self, tag_ids: list):
        valid_ids = []
        for tid in tag_ids:
            tid = tid.strip()
            if tid.isdigit() and Tag.objects.filter(id=int(tid)).exists():
                valid_ids.append(int(tid))
        return valid_ids

    def process_row(self, row: dict, **kwargs):
        print(row)
        print("=====================================================================================")
        fail_reasons = []
        product_name = row.get("name", "").strip()
        if not product_name:
            fail_reasons.append("Product name is required.")
        description = row.get("description", "").strip()
        if not description:
            fail_reasons.append("Product description is required.")
        color = row.get("color", "").strip()
        if not color:
            fail_reasons.append("Product color is required.")
        collection_ids = row.get("collection_ids", "").strip().split(",")
        if not collection_ids or not all(cid.strip().isdigit() for cid in collection_ids):
            fail_reasons.append("At least one valid collection_id is required.")
        image1 = row.get("image1_aws_url", "").strip()
        if not image1:
            fail_reasons.append("At least one image (image1) is required.")
        url_slug = row.get("url_slug", "").strip()
        fabric = row.get("fabric", "").strip()
        category_ids = row.get("category_ids", "").strip().split(",")
        occasion_ids = row.get("occasion_ids", "").strip().split(",")
        tag_ids = row.get("tag_ids", "").strip().split(",")
        image2 = row.get("image2_aws_url", "").strip()
        image3 = row.get("image3_aws_url", "").strip()
        image4 = row.get("image4_aws_url", "").strip()
        image5 = row.get("image5_aws_url", "").strip()
        
        product = Product.objects.filter(display_name=product_name, color=color).first()
        if product:
            fail_reasons.append("Product with the same name and color already exists.")
        
        if fail_reasons:
            return False, fail_reasons
        
        product = Product()
        product.display_name = product_name
        product.description = description
        product.color = color
        product.primary_image = image1
        product.save()
        if fabric:
            product.fabric = fabric
        # if url_slug:
        #     product.url_slug = url_slug
        
        valid_collection_ids = self.validate_collection_ids(collection_ids)
        if not valid_collection_ids:
            fail_reasons.append("No valid collection_ids found.")
            return False, fail_reasons
        product.collections.set(Collection.objects.filter(id__in=valid_collection_ids))

        valid_category_ids = self.validate_category_ids(category_ids)
        if not valid_category_ids:
            fail_reasons.append("No valid category_ids found.")
            return False, fail_reasons
        product.categories.set(Category.objects.filter(id__in=valid_category_ids))

        valid_occasion_ids = self.validate_occasion_ids(occasion_ids)
        if not valid_occasion_ids:
            fail_reasons.append("No valid occasion_ids found.")
            return False, fail_reasons
        product.occasions.set(Occasion.objects.filter(id__in=valid_occasion_ids))

        valid_tag_ids = self.validate_tag_ids(tag_ids)
        if not valid_tag_ids:
            fail_reasons.append("No valid tag_ids found.")
            return False, fail_reasons
        product.tags.set(Tag.objects.filter(id__in=valid_tag_ids))

        product.save()
        row["product_id"] = product.id

        image_urls = [image1, image2, image3, image4, image5]
        order = 0
        for img_url in image_urls:
            if img_url:
                ProductImage.objects.create(product=product, image_url=img_url, sort_order=order)
                order += 1

        return True, row

    def post_upload_changes(self, response_list_of_dict, **kwargs):
        pass

    def pre_upload_changes(self, response_list_of_dict, **kwargs):
        bucket = AWSBuckets.PRODUCT_IMAGE_BUCKET
        prefix = ''
        max_w = ImageDimensions.WIDTH
        max_h = ImageDimensions.HEIGHT
        workers = 10
        force_format = 'PNG'

        updated_data = [{**item,
                         "image1_aws_url": "",
                         "image2_aws_url": "",
                         "image3_aws_url": "",
                         "image4_aws_url": "",
                         "image5_aws_url": ""
                         } for item in response_list_of_dict]

        return run_pipeline(
            updated_data,
            bucket,
            max_w,
            max_h,
            workers,
            prefix,
            force_format)
