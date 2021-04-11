from backend.PostureService import PostureService
from backend.PostureRepository import PostureRepository
from backend.Posture import Posture

posture = Posture(0, 0, 0, 0, 0, 0, 0, 0, 0, 'test')

posture_service = PostureService()
print(posture_service.get_postures_by_user_id(posture))
