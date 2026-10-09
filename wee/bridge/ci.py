class NotConfiguredCIAdapter:
    provider_type='NOT_CONFIGURED'
    def trigger(self,commit_sha): return {'status':'NOT_CONFIGURED','reason':'CI provider adapter unavailable','commit_sha':commit_sha}
    def status(self,run_id): return {'status':'NOT_CONFIGURED','reason':'CI provider adapter unavailable','run_id':run_id}
    def result(self,run_id): return {'status':'NOT_CONFIGURED','reason':'CI provider adapter unavailable','run_id':run_id}
