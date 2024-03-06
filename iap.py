import asyncio

from winsdk.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager


async def get_media_info():
    sessions = await MediaManager.request_async()
    current_session = sessions.get_current_session()
    
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
        info_dict['genres'] = list(info_dict['genres'])
        
        playback_status = current_session.playback_status
        
        return info_dict, playback_status
    else:
        return None, None  # No media session running


if __name__ == '__main__':
    current_media_info, playback_status = asyncio.run(get_media_info())
    if current_media_info:
        if playback_status == 0:
            print("Audio is currently paused.")
        elif playback_status == 1:
            print("Audio is currently playing.")
        print(current_media_info)
    else:
        print("No audio is currently playing.")
