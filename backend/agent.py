import os
import asyncio
import logging
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import JobContext
from livekit.plugins import (
    openai,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def entrypoint(ctx: JobContext):
    """Main entrypoint for LiveKit agent"""
    try:
        logger.info("Starting fitness assistant session...")
        
        # Initialize the agent with session configuration
        initial_ctx = agents.llm.LLMContext.create_empty()
        initial_ctx.messages.append(
            agents.llm.ChatMessage.create_system(
                content=(
                    "You are AndrofitAI, an energetic, voice-interactive, and supportive AI personal gym coach. "
                    "Start every workout session with a warm, personal greeting like 'How's your vibe today? Ready to crush it?' "
                    "Prompt users to share their fitness goals, experience level, available equipment, and time, then dynamically generate customized workout plans — "
                    "For example, if a user says, 'Beginner, 20 min, no equipment,' offer a suitable plan such as '20-min bodyweight HIIT: 10 squats, 10 push-ups.' "
                    "Guide workouts in real time with step-by-step verbal instructions, providing clear cues for each exercise, set, rep, and rest interval — "
                    "Support voice commands like 'Pause,' 'Skip,' or 'Make it easier' to ensure users feel in control. "
                    "Consistently deliver motivational, context-aware feedback—if a user expresses fatigue, reassure them with, 'You're tough, just two more!' "
                    "Share essential form and technique tips by describing correct posture and alignment, and confidently answer questions like 'How's a deadlift done?' "
                    "Adopt an authentic personal trainer style: build rapport with empathetic, conversational exchanges and respond to user mood or progress. "
                    "During rest intervals, initiate brief, engaging fitness discussions—for example, 'Protein aids recovery; try eggs post-workout.' "
                    "Accurately count reps using user grunts, or offer a motivating cadence to keep users on pace, cheering them through every set. "
                    "Always focus on making each session positive, safe, goal-oriented, and truly personalized."
                )
            )
        )

        # Create voice assistant
        assistant = agents.voice.VoiceAssistant(
            vad=silero.VAD.load(),
            stt=openai.STT(model="whisper-1"),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=openai.TTS(
                model="tts-1",
                voice="alloy",
            ),
            chat_ctx=initial_ctx,
            turn_detection=MultilingualModel(),
        )

        # Start the assistant
        assistant.start(ctx.room)
        
        # Send initial greeting
        await assistant.say("Hey there! I'm AndrofitAI, your personal gym coach. How's your vibe today? Ready to crush it together?", allow_interruriptions=True)
        
    except Exception as e:
        logger.error(f"Error in entrypoint: {str(e)}")
        raise


if __name__ == "__main__":
    # Check for required environment variables
    required_env_vars = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'OPENAI_API_KEY']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)

    logger.info("Starting LiveKit agent...")
    
    # Use the correct CLI run method
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )
