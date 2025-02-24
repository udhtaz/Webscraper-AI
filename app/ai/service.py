from sqlmodel.ext.asyncio.session import AsyncSession
import logging
from sqlmodel import select

from app.db import Event
from .schemas import AIInputModel
from app.utils import get_all_events_table

logging.basicConfig(level=logging.INFO)

class AIService:
    async def generate_events_table(
        self, region_data: AIInputModel, session: AsyncSession,
    ):
        """
        Processes the AIInputModel payload, fetches event data, and saves to the database.
        """

        country = region_data.country
        city = region_data.city
        model = region_data.model 
        is_db = region_data.is_db  

        event_df = get_all_events_table(country, city, model)

        logging.info(f"{event_df}")

        generated_table = event_df.to_dict('records')

        if is_db:
            logging.info(f"Saving to Database...")

            # Organize events by name
            formatted_event_dict = {}
            for event_details in generated_table:
                event_name = event_details['event_name']
                if event_name in formatted_event_dict:
                    formatted_event_dict[event_name].append(event_details)
                else:
                    formatted_event_dict[event_name] = [event_details]

            # Process each event
            for event, event_list in formatted_event_dict.items():
                try:
                    logging.info(f"{'=' * 5} Processing Event: {event} {'=' * 5}")

                    # Extract event details
                    event_details = event_list[0]
                    event_category = event_details['event_category']
                    event_location = event_details['event_location']
                    venue = event_details['venue']
                    event_time = event_details['event_time']
                    event_url = event_details['event_url']
                    image_url = event_details.get('image_url', None)  # Optional
                    eventbrite_id = event_details['event_id']
                    event_description = event_details['event_description']

                    # Check if event exists asynchronously
                    query = select(Event).where(
                        (Event.event_name == event) &
                        (Event.event_location == event_location) &
                        (Event.eventbrite_id == eventbrite_id) &
                        (Event.event_time == event_time) &
                        (Event.model == model)
                    )

                    existing_event = await session.exec(query)
                    existing_event = existing_event.first()

                    if existing_event:
                        event_id = existing_event.id
                    else:
                        new_event = Event(
                            event_name=event,
                            event_category=event_category,
                            eventbrite_id=eventbrite_id,
                            event_location=event_location,
                            venue=venue,
                            event_time=event_time,
                            event_url=event_url,
                            image_url=image_url,
                            event_description=event_description,
                            model=model,
                        )

                        session.add(new_event)
                        await session.commit()
                        await session.refresh(new_event)

                        event_id = new_event.id

                except Exception as e:
                    logging.error(f"Error processing event {event}: {e}")

        return {"data": generated_table}
