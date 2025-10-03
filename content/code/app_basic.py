from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, LikeEvent

client = TikTokLiveClient(unique_id="kohcun")

# Event connect
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print("? Connected to Room ID:", client.room_id)

# Event comment
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    print(f">> {event.user.nickname}: {event.comment}")

# Event gift
@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    gift_name = getattr(event.gift, "name", "Unknown Gift")
    count = getattr(event.gift, "repeat_count", 1)
    print(f"?? {event.user.nickname} sent {gift_name} x{count}")

# Event like
@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    total = getattr(event, "total_likes", None)
    if total is not None:
        print(f"?? {event.user.nickname} tapped like! Total likes: {total}")
    else:
        print(f"?? {event.user.nickname} tapped like! (+{event.count})")

if __name__ == '__main__':
    client.run()
