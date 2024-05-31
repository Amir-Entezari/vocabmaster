from ninja import NinjaAPI
from vocabulary.api import router as vocabulary_router
from users.api import router as users_router
api = NinjaAPI(
    title="Vocabulary Master",
    urls_namespace='public_api',
)
api.add_router("", vocabulary_router)
api.add_router("/users", users_router)
