
from crud.base import CRUDBase
from models.models import Tasks


class CRUDTasks(CRUDBase[Tasks, Tasks, Tasks]):
    pass


tasks = CRUDTasks(Tasks)
