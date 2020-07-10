#!/usr/bin/env python3

import asyncio
import iterm2

"""
Disables background image when not in fullscreen.
"""
async def main(connection):
    app = await iterm2.async_get_app(connection)
    images = {}

    async def get_profile_for_session(session):
        return await session.async_get_profile()

    async def set_use_background_image_path(w, use_path):
        change = iterm2.LocalWriteOnlyProfile()
        tasks = []
        for tab in w.tabs:
            for session in tab.sessions:
                profile = await get_profile_for_session(session)
                if use_path:
                    change.set_background_image_location(images[profile.name])
                else:
                    change.set_background_image_location(images["disabled"])

            tasks.append(session.async_set_profile_properties(change))

        await asyncio.gather(*tasks) 

    async def update():
        if not images:
            images["disabled"] = ""
            for w in app.terminal_windows:
                for tab in w.tabs:
                    for session in tab.sessions:
                        profile = await get_profile_for_session(session)
                        images[profile.name] = profile._simple_get("Background Image Location")
        tasks = []
        for w in app.terminal_windows:
            style = await w.async_get_variable("style")
            if style == "non-native full screen" or style == "native full screen":
                tasks.append(set_use_background_image_path(w, True))
            else:
                tasks.append(set_use_background_image_path(w, False))
        if tasks:
            await asyncio.gather(*tasks)

    async def watch_for_style_changes():
        async with iterm2.VariableMonitor(connection, iterm2.VariableScopes.WINDOW, "style", "all") as mon:
            while True:
                theme = await mon.async_get()
                await update()

    async def watch_for_layout_changes():
        async with iterm2.LayoutChangeMonitor(connection) as mon:
            while True:
                await mon.async_get()
                await update()

    await update()

    asyncio.create_task(watch_for_style_changes())
    asyncio.create_task(watch_for_layout_changes())

iterm2.run_forever(main, True)
