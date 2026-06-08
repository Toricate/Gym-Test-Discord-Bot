import discord
from discord.ext import commands
from discord import ui
from PIL import Image, ImageDraw
import io
import asyncio

# --- CONFIGURATION ---
TOKEN = 'DISCORD BOT TOKEN' 
TEMPLATE_FILE = "Gym Compass.png"
CATEGORY_NAME = "Chemical Test"

intents = discord.Intents.default()
intents.members = True 
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

QUESTIONS = [
    # X-AXIS: NATURAL (-2) VS CHEMICAL (+2)
    {"t": "Performance-enhancing substances are a modern necessity for those reaching their genetic limit.", "a": "x"},
    {"t": "An individual’s 'natural' status is maintained as long as they only use substances prescribed by a doctor.", "a": "x"},
    {"t": "The health risks associated with muscle-building chemicals are often exaggerated.", "a": "x"},
    {"t": "Natural bodybuilding is an idealistic concept that is rarely seen at the top level.", "a": "x"},
    {"t": "Healing peptides and growth hormones should be viewed as recovery tools rather than 'cheating'.", "a": "x"},
    {"t": "A physique built with chemical assistance is just as impressive as one built naturally.", "a": "x"},
    {"t": "Anyone serious about muscle growth should eventually consider hormone replacement therapy.", "a": "x"},
    {"t": "The line between legal supplements and banned substances is mostly just a social rule.", "a": "x"},
    {"t": "I would prioritize a world-class physique over the long-term health of my internal organs.", "a": "x"},
    {"t": "The best investment a lifter can make is in regular blood work and a trusted supplier.", "a": "x"},
    {"t": "If you aren't using everything available to help you grow, you aren't truly committed.", "a": "x"},
    {"t": "Knowing how to restore natural hormones (PCT) is more critical than knowing how to diet.", "a": "x"},
    {"t": "Using weight-loss injections like Retatrutide is a valid way to stay lean year-round.", "a": "x"},
    {"t": "Pre-workout is essential; if I am not shaking from stimulants, the workout is a waste.", "a": "x"},
    {"t": "Taking multiple scoops of high-stimulant pre-workout is necessary for high-level training.", "a": "x"},
    # Y-AXIS: FORM (-2) VS EGO (+2)
    {"t": "Do you agree with the saying 'if the bar isnt bending youre just pretending'?", "a": "y"},
    {"t": "Using a bit of 'swing' or momentum is necessary to break through a strength plateau.", "a": "y"},
    {"t": "The total weight on the bar is a more accurate metric of progress than muscle feel.", "a": "y"},
    {"t": "A 100kg bench with a slight bounce is better than 60kg with a perfect pause.", "a": "y"},
    {"t": "Perfect form is often used as an excuse by people who are afraid to lift heavy.", "a": "y"},
    {"t": "The psychological boost of a new PB is worth the minor risk of technique slipping.", "a": "y"},
    {"t": "Lifting belts and straps should be used primarily to move more weight, not just for safety.", "a": "y"},
    {"t": "Small isolation exercises are a waste of time compared to moving heavy weight on big lifts.", "a": "y"},
    {"t": "A failed rep where form broke down is still a success if you forced the weight to move.", "a": "y"},
    {"t": "You should train to impress the people watching you in the gym.", "a": "y"},
    {"t": "Lifting slowly and controlled is less effective for building power than lifting explosively.", "a": "y"},
    {"t": "The risk of a minor injury is an acceptable trade-off for a legendary heavy session.", "a": "y"},
    {"t": "Ego lifting is actually just a label for training with maximum intensity.", "a": "y"},
    {"t": "If you aren't making noise or dropping weights, you aren't training at your true limit.", "a": "y"},
    {"t": "The aesthetic of the lift (how many plates are on the bar) is as important as the technique.", "a": "y"}
]

def get_gym_status(x, y):
    if x > 18: x_lab = "Far Chemical"
    elif x > 6: x_lab = "Moderate Chemical"
    elif x < -18: x_lab = "Far Natural"
    elif x < -6: x_lab = "Moderate Natural"
    else: x_lab = "Neutral"

    if y > 18: y_lab = "Far Ego"
    elif y > 6: y_lab = "Moderate Ego"
    elif y < -18: y_lab = "Far Form"
    elif y < -6: y_lab = "Moderate Form"
    else: y_lab = "Neutral"

    mapping = {
        ("Far Chemical", "Far Ego"): "The Tren-Titan",
        ("Far Natural", "Far Form"): "The Zen Master",
        ("Far Chemical", "Far Form"): "The Bio-Hacker",
        ("Far Natural", "Far Ego"): "The Raw Chaos",
        ("Neutral", "Neutral"): "The Casual Lifter"
    }
    return mapping.get((x_lab, y_lab), f"{x_lab} / {y_lab}")

class CompassView(ui.View):
    def __init__(self, user, channel):
        super().__init__(timeout=600)
        self.user = user
        self.channel = channel
        self.current_q = 0
        self.x_score = 0
        self.y_score = 0

    async def send_question(self):
        q = QUESTIONS[self.current_q]
        embed = discord.Embed(title=f"Gym Compass: Question {self.current_q + 1}/30", 
                              description=f"**{q['t']}**", color=0x2b2d31)
        await self.channel.send(content=self.user.mention, embed=embed, view=self)

    async def handle_click(self, interaction, val):
        if interaction.user != self.user: return
        axis = QUESTIONS[self.current_q]["a"]
        if axis == "x": self.x_score += val
        else: self.y_score += val
        self.current_q += 1
        if self.current_q < len(QUESTIONS):
            q = QUESTIONS[self.current_q]
            embed = discord.Embed(title=f"Question {self.current_q + 1}/30", description=f"**{q['t']}**", color=0x2b2d31)
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            await self.finish(interaction)

    @ui.button(label="Strongly Agree", style=discord.ButtonStyle.green)
    async def sa(self, i, b): await self.handle_click(i, 2)
    @ui.button(label="Agree", style=discord.ButtonStyle.secondary)
    async def a(self, i, b): await self.handle_click(i, 1)
    @ui.button(label="Disagree", style=discord.ButtonStyle.secondary)
    async def d(self, i, b): await self.handle_click(i, -1)
    @ui.button(label="Strongly Disagree", style=discord.ButtonStyle.danger)
    async def sd(self, i, b): await self.handle_click(i, -2)

    async def finish(self, interaction):
        await interaction.response.defer()
        status = get_gym_status(self.x_score, self.y_score)
        
        try:
            with Image.open(TEMPLATE_FILE) as img:
                draw = ImageDraw.Draw(img)
                w, h = img.size
                
                # --- CALIBRATED MATH ---
                # Based on your image, the colored grid starts roughly 135px in from each side.
                grid_margin = 135 
                
                # Calculate the bounds of the actual colored squares
                min_x, max_x = grid_margin, w - grid_margin
                min_y, max_y = grid_margin, h - grid_margin
                
                center_x, center_y = w / 2, h / 2
                
                # Max score is 30. We map that score to the distance between center and grid edge.
                pixel_x = center_x + (self.x_score / 30) * (center_x - grid_margin)
                pixel_y = center_y - (self.y_score / 30) * (center_y - grid_margin)
                
                # CLAMPING: This ensures the dot stays inside the colors no matter what
                pixel_x = max(min_x, min(max_x, pixel_x))
                pixel_y = max(min_y, min(max_y, pixel_y))

                r = 18 # Slightly larger dot for visibility
                draw.ellipse([pixel_x-r, pixel_y-r, pixel_x+r, pixel_y+r], fill="red", outline="white", width=4)
                
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                file = discord.File(buf, filename="result.png")
        except FileNotFoundError:
            await self.channel.send(f"Error: '{TEMPLATE_FILE}' not found!")
            return

        await self.channel.send(f"Test complete! Your Gym Rank is: **{status}**", file=file)
        await asyncio.sleep(60)
        await self.channel.delete()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def start(ctx):
    category = discord.utils.get(ctx.guild.categories, name=CATEGORY_NAME)
    if category is None:
        await ctx.send(f"⚠️ Error: Please create a category named '{CATEGORY_NAME}'!")
        return

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
        ctx.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
    }
    channel = await ctx.guild.create_text_channel(f"gym-test-{ctx.author.name}", overwrites=overwrites, category=category)
    view = CompassView(ctx.author, channel)
    await view.send_question()
    try: await ctx.message.delete()
    except: pass

bot.run(TOKEN)