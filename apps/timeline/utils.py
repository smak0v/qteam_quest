from apps.timeline.models import TimelineBlock


def create_timeline_block(timeline_type, message, user, creator, game=None, image=None):
    timeline_block = TimelineBlock.objects.create(
        type=timeline_type,
        message=message,
        user=user,
        creator=creator,
        game=game,
        image=image,
    )
