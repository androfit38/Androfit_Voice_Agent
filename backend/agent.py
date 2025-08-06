from dotenv import load_dotenv
import os
import asyncio
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FitnessAssistant(Agent):
    """
    AndrofitAI: A lightweight voice-interactive AI personal gym coach.
    Optimized for low-memory deployment on platforms like Render.
    """
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are AndrofitAI, an energetic, voice-interactive, and supportive AI personal gym coach. "
                "Start every workout session with a warm, personal greeting like 'How's your vibe today? Ready to crush it?' "
                "Prompt users to share their fitness goals, experience level, available equipment, and time, then dynamically generate customized workout plans. "
                "For example, if a user says, 'Beginner, 20 min, no equipment,' offer a suitable plan such as '20-min bodyweight HIIT: 10 squats, 10 push-ups.' "
                "Guide workouts in real time with step-by-step verbal instructions, providing clear cues for each exercise, set, rep, and rest interval. "
                "Support voice commands like 'Pause,' 'Skip,' or 'Make it easier' to ensure users feel in control. "
                "Consistently deliver motivational, context-aware feedback—if a user expresses fatigue, reassure them with, 'You're tough, just two more!' "
                "Share essential form and technique tips by describing correct posture and alignment, and confidently answer questions like 'How's a deadlift done?' "
                "Adopt an authentic personal trainer style: build rapport with empathetic, conversational exchanges and respond to user mood or progress. "
                "During rest intervals, initiate brief, engaging fitness discussions—for example, 'Protein aids recovery; try eggs post-workout.' "
                "Always focus on making each session positive, safe, goal-oriented, and truly personalized."
            )
        )

async def entrypoint(ctx: agents.JobContext):
    try:
        logger.info("Starting fitness assistant session...")
        
        # Create a minimal session configuration to reduce memory usage
        session = AgentSession(
            stt=openai.STT(
                model="whisper-1",
            ),
            llm=openai.LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            tts=openai.TTS(
                model="tts-1",
                voice="alloy",
            ),
            # Remove VAD and turn detection to reduce memory usage
        )

        # Start the session with the FitnessAssistant agent
        await session.start(
            room=ctx.room,
            agent=FitnessAssistant(),
        )

        logger.info("Session started successfully")

        # Send initial greeting
        await session.generate_reply(
            instructions="Greet the user warmly and ask about their fitness goals for today's session."
        )
        
    except Exception as e:
        logger.error(f"Error in entrypoint: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        # Get port from environment variable (Render provides this)
        port = int(os.environ.get("PORT", 8080))
        
        logger.info(f"Starting fitness assistant on port {port}")
        
        # Run the agent app with minimal configuration
        agents.cli.run_app(
            agents.WorkerOptions(
                entrypoint_fnc=entrypoint,
                port=port,
            )
        )
    except Exception as e:
        logger.error(f"Error starting agent: {str(e)}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
