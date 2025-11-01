from marshmallow import fields, Schema, pre_dump


class GenericBulkUploaderResponseSchema(Schema):
 response_file_link = fields.Str(data_key="responseFileLink", default="")
 status = fields.Str(data_key="status", default="PROCESSING")
 process_start_time = fields.DateTime(data_key="processStartTime")
 process_end_time = fields.DateTime(data_key="processEndTime")
 is_completed = fields.Boolean(data_key="isCompleted", default=False)
 

class GenericBulkUploaderRequestSchema(Schema):
    upload_type = fields.Str(data_key="uploadType")
    status = fields.Str(data_key="status")
    params_dict = fields.Dict(data_key="paramsDict")
    request_file_link = fields.Str(data_key="requestFileLink")
    id = fields.Int(data_key="id")
    response = fields.Nested(GenericBulkUploaderResponseSchema())
    created_on = fields.DateTime(data_key="createdOn")
    admin_user = fields.Str(data_key="user")