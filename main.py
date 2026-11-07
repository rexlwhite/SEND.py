import os
import discord
from keep_alive import keep_alive
from discord.ext import commands

# ตั้งค่า Intents (ต้องเปิด Server Members Intent และ Message Content Intent ใน Discord Developer Portal ด้วย)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# 1. คำสั่งส่งข้อความถึงทุกคนในช่อง (Announcement / Broadcast)
# ใช้งาน: !send <ข้อความ> หรือใส่ @everyone
@bot.command(name='send', help='ให้บอทส่งข้อความไปยังแชท')
@commands.has_permissions(administrator=True) # กำหนดให้ใช้ได้เฉพาะแอดมิน (เปลี่ยนได้ตามต้องการ)
async def send(ctx, *, message: str):
    # ลบข้อความคำสั่งของคนที่พิมพ์ เพื่อความสะอาดของแชท (ถ้าต้องการ)
    await ctx.message.delete()
    # ส่งข้อความ
    await ctx.send(f"{message}") # หากไม่อยากแท็ก @everyone ให้ลบคำว่า @everyone ออก


# 2. คำสั่งเคลียร์ข้อความ (Purge / Clear)
# ใช้งาน: !clear <จำนวน> เช่น !clear 10
@bot.command(name='clear', aliases=['purge'], help='ลบข้อความตามจำนวนที่กำหนด')
@commands.has_permissions(manage_messages=True) # ต้องมีสิทธิ์จัดการข้อความ
async def clear(ctx, amount: int):
    # ลบข้อความคำสั่ง + จำนวนที่ระบุ
    deleted = await ctx.channel.purge(limit=amount + 1)
    # ส่งข้อความแจ้งเตือนแล้วลบอัตโนมัติใน 3 วินาที
    msg = await ctx.send(f'>>> **เรียลไวท์ลบแล้ว {len(deleted) - 1} ข้อความ**', delete_after=3)


# จัดการกรณีไม่มีสิทธิ์ใช้งานคำสั่ง
@send.error
@clear.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(">>> **คุณไม่มีสิทธิ์ในการใช้คำสั่งนี้!**", delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(">>> **กรุณากรอกข้อมูลให้ครบถ้วนด้วยครับ!**", delete_after=5)

keep_alive()

# ใส่ Token ของบอทคุณตรงนี้
bot.run(os.getenv('TOKEN'))