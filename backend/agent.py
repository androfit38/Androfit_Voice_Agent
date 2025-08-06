from dotenv import load_dotenv
import os
import asyncio
import logging

from livekit import agents
from livekit.agents import AutoSubscribe, AgentSession, Agent, JobContext
from livekit.plugins import openai

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FitnessAssistant(Agent):
    """
    AndrofitAI: A lightweight voice-interactive AI personal gym coach.
    Optimized for deployment with proper error handling.
    """
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are AndrofitAI, an energetic and supportive AI personal gym coach. "
                "Greet users warmly and ask about their fitness goals. "
                "Create personalized workout plans based on their experience level, available time, and equipment. "
                "Provide clear, step-by-step exercise instructions with proper form cues. "
                "Offer motivational support throughout the workout session. "
                "Answer fitness-related questions and provide helpful tips. "
                "Keep responses concise but encouraging."
            )
        )

    async def astart(self, ctx: agents.JobContext) -> None:
        """Agent startup method"""
        logger.info("FitnessAssistant started")
        await super().astart(ctx)

async def entrypoint(ctx: JobContext):
    """Main entry point for the agent"""
    try:
        logger.info("Initializing fitness assistant...")
        
        # Validate environment variables
        required_env_vars = ["OPENAI_API_KEY", "LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {missing_vars}")
            raise ValueError(f"Missing environment variables: {missing_vars}")
        
        # Initialize components with error handling
        try:
            stt = openai.STT(
                model="whisper-1",
                language="en",  # Specify language to reduce processing
            )
            logger.info("STT initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize STT: {e}")
            raise

        try:
            llm = openai.LLM(
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=150,  # Limit response length to reduce latency
            )
            logger.info("LLM initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            raise

        try:
            tts = openai.TTS(
                model="tts-1",
                voice="alloy",
            )
            logger.info("TTS initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            raise

        # Create agent session
        session = AgentSession(
            stt=stt,
            llm=llm,
            tts=tts,
            auto_subscribe=AutoSubscribe.AUDIO_ONLY,  # Only subscribe to audio
        )
        
        logger.info("Agent session created")

        # Create and start the agent
        agent = FitnessAssistant()
        
        await session.start(
            room=ctx.room,
            agent=agent,
        )

        logger.info("Session started successfully")

        # Send initial greeting
        try:
            await session.generate_reply(
                instructions="Give a brief, energetic greeting and ask the user about their fitness goals for today."
            )
            logger.info("Initial greeting sent")
        except Exception as e:
            logger.error(f"Failed to send initial greeting: {e}")
            # Continue without greeting rather than crashing

    except Exception as e:
        logger.error(f"Error in entrypoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        # Get port from environment variable
        port = int(os.environ.get("PORT", 8080))
        
        logger.info(f"Starting fitness assistant on port {port}")
        logger.info(f"OpenAI API Key present: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
        logger.info(f"LiveKit URL present: {'Yes' if os.getenv('LIVEKIT_URL') else 'No'}")
        
        # Run the agent with proper configuration
        agents.cli.run_app(
            agents.WorkerOptions(
                entrypoint_fnc=entrypoint,
                port=port,
            )
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Error starting agent: {str(e)}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1
