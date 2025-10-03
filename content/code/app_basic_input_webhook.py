from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, LikeEvent
import httpx
import asyncio

WEBHOOK_URL = "http://103.171.85.170/webhook/tiktok"

# === Input Unique ID TikTok secara dinamis ===
unique_id = input("Masukkan Unique ID (tanpa @): ").strip()

# Buat client dengan unique_id hasil input
client = TikTokLiveClient(unique_id=unique_id)


# Fungsi helper untuk kirim ke webhook
async def send_to_webhook(payload: dict):
    try:
        async with httpx.AsyncClient() as http_client:
            r = await http_client.post(WEBHOOK_URL, json=payload, timeout=10)
            print(f"[Webhook] Sent ({r.status_code})")
    except Exception as e:
        print(f"[Webhook Error] {e}")


# Event connect
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    data = {"event": "connect", "room_id": client.room_id}
    print("? Connected to Room ID:", client.room_id)
    await send_to_webhook(data)


# Event comment
@client.on(CommentEvent)
async def on_comment(event: CommentEvent):
    data = {
        "event": "comment",
        "user": event.user.nickname,
        "comment": event.comment
    }
    print(f"?? {event.user.nickname}: {event.comment}")
    await send_to_webhook(data)


# Event gift
@client.on(GiftEvent)
async def on_gift(event: GiftEvent):
    gift_name = getattr(event.gift, "name", "Unknown Gift")
    count = getattr(event.gift, "repeat_count", 1)

    data = {
        "event": "gift",
        "user": event.user.nickname,
        "gift": gift_name,
        "count": count
    }
    print(f"?? {event.user.nickname} sent {gift_name} x{count}")
    await send_to_webhook(data)


# Event like
@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    total = getattr(event, "total_likes", None)
    if total is not None:
        msg = f"?? {event.user.nickname} tapped like! Total likes: {total}"
    else:
        msg = f"?? {event.user.nickname} tapped like! (+{event.count})"

    data = {
        "event": "like",
        "user": event.user.nickname,
        "count": event.count,
        "total": total
    }
    print(msg)
    await send_to_webhook(data)


if __name__ == '__main__':
    client.run()
