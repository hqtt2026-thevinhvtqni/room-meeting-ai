from __future__ import annotations
class AuthorityPolicy:
    def can_commit(self,work_context): return {'allowed':False,'status':'BLOCKED','policy_blocked':True,'reason':'ROOM-HOP authority not granted'}
    def can_push(self,work_context): return {'allowed':False,'status':'BLOCKED','policy_blocked':True,'reason':'ROOM-HOP authority not granted'}
    def can_verify_remote(self,work_context): return {'allowed':False,'status':'BLOCKED','policy_blocked':True,'reason':'GitHub gateway not configured'}
