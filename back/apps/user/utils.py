from .models import MyUser
import uuid

# ユニークなIDを生成
def generate_unique_id():
    uid = str(uuid.uuid4())[:15]  # UUIDを生成し、最初の15文字を取得
    while MyUser.objects.filter(userid=uid).exists():
        uid = str(uuid.uuid4())[:15]  # 重複している場合は新しいUUIDを生成
    return uid