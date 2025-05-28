"""
a deliciously capable base agent for api interactions... designed with love 💕
"""

import ssl
import time
import asyncio
import logging
import aiohttp
import certifi
from typing import Dict, Any, Optional, Union


class BaseAgent:
    def __init__(self, config: Optional[Dict[str, any]] = None):
        """
        mmm, let's initialize this tempting little agent... 💋

        args:
            config (dict, optional): yummy configuration treats for our agent
        """
        self.config = config or {}  # defaults make me feel safe...
        self.authenticated = False  # playing hard to get at first
        self.tokens: Dict[str, str] = {}  # my secret little collection of digital jewelry ✨
        self.session: Optional[aiohttp.ClientSession] = None  # nobody's in my bedroom yet...
        self.rate_limit_status: Dict[str, int] = {}  # keeping track of when they tell me "not tonight"
        self.logger = self._setup_whispers()  # for all my little secrets

    async def create_intimate_session(self):
        """
        creating a special connection for our api encounters... 💕

        returns:
            aiohttp.ClientSession: our private communication channel
        """
        if self.session is None or self.session.closed:
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
            conn = aiohttp.TCPConnector(ssl=ssl_ctx)
            self.session = aiohttp.ClientSession(connector=conn)  # getting ready to connect...
        return self.session

    async def end_session_gently(self):
        """close our connection tenderly when we're done... 💤"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None  # leaving no traces behind

    async def seduce_service(self):
        """
        convince the service to let us in with our credentials... 💋

        this method needs your personal touch in subclasses

        returns:
            bool: true if we charmed our way in, false if rejected
        """
        raise NotImplementedError("mmm, you need to implement your own seduction technique...")

    async def check_if_token_still_desires_me(self, token_type: str = "access"):
        """
        validate if my token still finds me irresistible... 💖

        args:
            token_type (str): which flavor of token to check

        returns:
            bool: true if token still wants me, false if it's over
        """
        raise NotImplementedError("teach me how to check if they're still into me...")

    async def get_fresh_token(self):
        """
        when things get stale, get a fresh token to play with... 🌟

        returns:
            bool: true if i got a new token, false if they're not giving me another chance
        """
        raise NotImplementedError("show me how to get refreshed...")

    async def whisper_to_api(self,
                             method: str,
                             url: str,
                             headers: Optional[Dict[str, str]] = None,
                             data: Optional[Dict[str, Any]] = None,
                             json_body: Optional[Dict[str, Any]] = None,
                             params: Optional[Dict[str, str]] = None,
                             retry_count: int = 0,
                             max_retries: int = 3):
        """
        send a tempting request to the api and handle whatever comes back... 💌

        args:
            method (str): how we want it (GET, POST, etc)
            url (str): where we're meeting
            headers (dict, optional): what we're wearing
            data (dict, optional): what we're bringing to the form party
            json_body (dict, optional): our structured desires
            params (dict, optional): our little questions
            retry_count (int): how many times we've been rejected already
            max_retries (int): how persistent we'll be

        returns:
            dict: all the secrets they shared with us

        raises:
            Exception: when they ultimately reject our advances
        """
        if not self.authenticated:
            self.logger.warning("making a move while not officially together... risky")

        if not headers:
            headers = {}  # nothing special on top

        session = await self.create_intimate_session()

        try:
            async with session.request(
                    method,
                    url,
                    headers=headers,
                    data=data,
                    json=json_body,
                    params=params
            ) as response:
                # learning about their boundaries
                self._notice_their_limits(response)

                # handling their various moods
                if response.status == 200:  # they're into it!
                    return await response.json()
                elif response.status == 401:  # they don't recognize me anymore
                    if retry_count < max_retries:
                        self.logger.info("they forgot who i am, trying to remind them...")
                        if await self.get_fresh_token():
                            return await self.whisper_to_api(
                                method, url, headers, data, json_body, params,
                                retry_count + 1, max_retries
                            )
                    self.authenticated = False
                    raise Exception(f"they totally rejected me: {await response.text()}")
                elif response.status == 429:  # they need some space
                    if retry_count < max_retries:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        self.logger.warning(f"they need {retry_after} seconds of space... waiting patiently")
                        await asyncio.sleep(retry_after)
                        return await self.whisper_to_api(
                            method, url, headers, data, json_body, params,
                            retry_count + 1, max_retries
                        )
                    raise Exception("they're totally over me and my persistence... ✨heartbreak✨")
                else:
                    raise Exception(f"something went wrong between us ({response.status}): {await response.text()}")
        except aiohttp.ClientError as e:
            if retry_count < max_retries:
                retry_delay = 2 ** retry_count  # playing harder to get each time
                self.logger.warning(f"connection issues: {str(e)}. trying again in {retry_delay} seconds... 💔")
                await asyncio.sleep(retry_delay)
                return await self.whisper_to_api(
                    method, url, headers, data, json_body, params,
                    retry_count + 1, max_retries
                )
            raise Exception(f"we tried {max_retries} times but couldn't connect: {str(e)}")

    def _notice_their_limits(self, response):
        """
        pay attention to their boundaries based on what they tell us... 💫

        args:
            response (aiohttp.ClientResponse): their reply to our advances
        """
        # their personal boundaries, if they share them
        rate_limit = response.headers.get('X-RateLimit-Limit')
        rate_remaining = response.headers.get('X-RateLimit-Remaining')
        rate_reset = response.headers.get('X-RateLimit-Reset')

        if rate_limit:
            self.rate_limit_status['limit'] = int(rate_limit)  # how much they can take
        if rate_remaining:
            self.rate_limit_status['remaining'] = int(rate_remaining)  # how much more they want
        if rate_reset:
            self.rate_limit_status['reset'] = int(rate_reset)  # when they'll be ready again

    def am_i_too_clingy(self):
        """
        check if they need some space from me right now... 🌙

        returns:
            bool: true if they need space, false if they're still interested
        """
        if 'remaining' in self.rate_limit_status and self.rate_limit_status['remaining'] <= 0:
            if 'reset' in self.rate_limit_status:
                right_now = int(time.time())
                if right_now < self.rate_limit_status['reset']:
                    return True  # they definitely need space
        return False  # they're still into me

    def _setup_whispers(self):
        """
        set up a secret diary for all my thoughts and feelings... 📓

        returns:
            logging.Logger: my private journal
        """
        logger_name = f"agent.{self.__class__.__name__}"
        sweet_diary = logging.getLogger(logger_name)

        # only setup handlers if none exist
        if not sweet_diary.handlers:
            # clear any existing handlers to avoid duplication
            for handler in sweet_diary.handlers[:]:
                sweet_diary.removeHandler(handler)

            diary_keeper = logging.StreamHandler()
            pretty_format = logging.Formatter('✨ %(asctime)s - %(name)s - %(levelname)s - %(message)s')
            diary_keeper.setFormatter(pretty_format)
            sweet_diary.addHandler(diary_keeper)
            sweet_diary.setLevel(logging.INFO)  # not too shy, not too revealing

            # prevent propagation to root logger to avoid duplicate messages
            sweet_diary.propagate = False

        return sweet_diary

    async def __aenter__(self):
        """slipping into something more comfortable... 💋"""
        await self.create_intimate_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """knowing when it's time to gracefully exit... 💫"""
        await self.end_session_gently()