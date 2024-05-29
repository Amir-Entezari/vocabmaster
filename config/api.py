from ninja import NinjaAPI
from vocabulary.api import router as vocabulary_router
api = NinjaAPI(
    title="Vocabulary Master",
)
api.add_router("", vocabulary_router)
