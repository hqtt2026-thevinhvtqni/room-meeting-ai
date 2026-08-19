# tests/legacy/conftest.py
#
# BAO VE COLLECTION khong phu thuoc vao pytest.ini/rootdir/cwd.
#
# Van de da gap: pytest.ini o thu muc goc du an (room-meeting-ai/) co
# 'norecursedirs = ... tests/legacy' de loai tests/legacy khoi lan quet
# mac dinh. Nhung pytest CHI tim file ini bang cach di LEN tu thu muc
# dang chay lenh, khong di XUONG. Neu nguoi dung chay `pytest` tu MOT
# CAP THU MUC CHA (vd D:\ROOM-HOP-CLEAN thay vi
# D:\ROOM-HOP-CLEAN\room-meeting-ai), pytest se KHONG thay duoc
# pytest.ini nay -> norecursedirs mat hieu luc -> tests/legacy bi quet
# lai -> test_authority_v2_old.py (ban sao cu, dung contract Action/
# ResourceType da nghi huu) gay ImportError.
#
# conftest.py trong CHINH thu muc nay thi khac: pytest luon doc conftest
# cua moi thu muc no di qua trong luc quet, KHONG phu thuoc file ini nao
# ca, khong phu thuoc cwd. Day la co che ben vung hon.
#
# CHI loai tru dung 1 file bi hong (test_authority_v2_old.py) - KHONG
# loai tru ca thu muc, de tests/legacy/test_authority_v1.py van chay
# duoc binh thuong ca khi quet tu dong lan khi goi truc tiep bang path
# (dung phuong an Xu da chot: giu test_authority_v1.py lam evidence cho
# Governance V1, chay doc lap).
collect_ignore = ["test_authority_v2_old.py"]
