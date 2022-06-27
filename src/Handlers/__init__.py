from .Handler import Handler
from .Mail import Mail
from .SquadCast import SquadCast

Handler.register("mail", Mail)
Handler.register("squadcast", SquadCast)
