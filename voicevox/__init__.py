"""
VOICEVOX engine wrapper for python3
Copyright © 2022 okaits#7534

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

import json
import os
import tempfile
import time
import urllib.parse
import urllib.request
import wave
from typing import Union

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # Disable pygame's welcome message
import pygame.mixer  # pylint: disable=E0401 C0413

class Server():
    """ Server class """
    def __init__(self, server: str = "localhost:50021") -> None:
        self.server = server

    def get_speakerid_list(self) -> dict:
        """ Get speaker id list """
        with urllib.request.urlopen(f"http://{self.server}/speakers") as speakers:
            speakerid_list = json.load(speakers)
        speakers = dict()
        for speaker in speakerid_list:
            for style in speaker['styles']:
                speakers[f"{speaker['name']} - {style['name']}"] = style['id']
        return speakers


class Query():
    """ Query class """
    def __init__(self, query: dict, request: Request, client: Client) -> None:
        self.query = query
        self.speaker = request.speaker
        self.client = client
        self.text = request.text

class Voice():
    """ Voice class """
    def __init__(self, data: bytes, query: Query) -> None:
        self.data = data
        self.query = query.query
        self.server = query.client.server
        self.speaker = query.speaker
        self.text = query.text

    def save(self, output) -> None:
        """ Save self.data to file """
        with open(output, "wb") as file:
            file.write(self.data)

    def play(self) -> None:
        """ Save self.data to tempfile, then play it """
        _, temppath = tempfile.mkstemp()
        with open(temppath, "wb") as temp:
            temp.write(self.data)
        with wave.open(temppath, "rb") as wavfile:
            frames = wavfile.getnframes()
            framerate = wavfile.getframerate()
        pygame.mixer.init()
        pygame.mixer.music.load(temppath)
        pygame.mixer.music.play(1)
        time.sleep(1.0 * frames / framerate)
        pygame.mixer.music.stop()

class Request():
    """ Request class """
    def __init__(self, client: Client, text: str, speaker: int) -> None:
        self.client = client
        self.output = ""
        self.speaker = speaker
        self.text = text
        self.query = []

    def request_query(self) -> Query:
        """ Request query json to server, then download it """
        url = f"http://{str(self.client.server)}/audio_query?speaker={str(self.speaker)}&text={urllib.parse.quote(self.text)}" #pylint: disable=C0301
        req = urllib.request.Request(url, method="POST")
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        try:
            with urllib.request.urlopen(req) as response:
                query = json.load(response)
        except urllib.error.URLError:
            print("Error: Something went wrong while connecting to the server."
                        "Please check your server, then please retry.")
            return urllib.error.URLError

        return Query(query, self, self.client)

    def request_voice(self, query: Query) -> Voice:
        """ Request voice to the server, then download it """
        query = json.dumps(query.query)
        data = query.encode("utf-8")
        url = f"http://{str(self.client.server)}/synthesis?speaker={str(self.speaker)}"
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as response:
            data = response.read()
        return Voice(data, self)


class Client():
    """ Client class """
    def __init__(self, server: Union[str, Server] = "localhost:50021") -> None:
        if isinstance(server, Server):
            self.server = server.server
        else:
            self.server = server

    def request(self, text: str, speaker: int = 3):
        """ Set self.text """
        return Request(self, text, speaker)
