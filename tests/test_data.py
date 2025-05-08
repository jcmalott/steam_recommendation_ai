STEAM_WISHLIST_URL = 'https://api.steampowered.com/IWishlistService/GetWishlist/v1'
STEAM_LIBRARY_URL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
STEAM_GAME_URL = 'https://store.steampowered.com/api/appdetails'
STEAM_USER_URL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
STEAM_API_KEY="test_api_key"
STEAM_USER_ID="76561198041511379"
STEAM_APPID=1144200

DATABASE_USER="test_user"
DATABASE_NAME="test_db"
DATABASE_PASSWORD="test_password"

# ------------------------
# -----  CHECK USER  -----
# ------------------------
CORRECT_USER_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
                "personaname": "Test User",
                "profileurl": "https://steamcommunity.com/id/testuser/",
                "avatarfull": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
                "realname": "Real Test Name",
                "loccountrycode": "US",
                "locstatecode": "CA"
            }
        ]
    }
}
ONLY_STEAMID_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
                "personaname": "",
                "profileurl": "",
                "avatarfull": "",
                "realname": "",
                "loccountrycode": "",
                "locstatecode": ""
            }
        ]
    }
}
EMPTY_USER_RESPONSE = {
    "response": {
        "players": []
    }
}
INVALID_USER_ID_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": "different_id",
                "personaname": "Test User",
                "profileurl": "https://steamcommunity.com/id/testuser/",
                "avatarfull": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
                "realname": "Real Test Name",
                "loccountrycode": "US",
                "locstatecode": "CA"
            }
        ]
    }
}
PARTIAL_USER_RESPONSE = {
    "response": {
        "players": [
            {
                "steamid": STEAM_USER_ID,
                # Missing other fields
            }
        ]
    }
}

# PROCESS DATA
CORRECT_USER_PROCESSED = {
    "steamid": STEAM_USER_ID,
    "persona_name": "Test User",
    "profile_url": "https://steamcommunity.com/id/testuser/",
    "avatar_full": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/test.jpg",
    "real_name": "Real Test Name",
    "country_code": "US",
    "state_code": "CA"
}
USER_ID_ONLY_PROCESSED = {
    "steamid": STEAM_USER_ID,
    "persona_name": "",
    "profile_url": "",
    "avatar_full": "",
    "real_name": "",
    "country_code": "",
    "state_code": ""         
}


# ------------------------
# ------  WISHLIST  ------
# ------------------------
CORRECT_WISHLIST_RESPONSE = {
    "response": {
        "items": [
            {
                "appid": 16900,
                "priority": 303,
                "date_added": 1689263421
            }
        ]
    }
}
PARTIAL_WISHLIST_RESPONSE = {
    "response": {
        "items": [
            {
                "appid": 16900,
            }
        ]
    }
}
EMPTY_WISHLIST_RESPONSE = {
    "response": {
        "items": [{}]
    }
}
DB_WISHLIST_RESPONSE = [
    ('76561198041511379',  362490, 253),
    ('76561198041511379',  362680, 132) 
]


# PROCESS DATA
CORRECT_WISHLIST_PROCESSED = [{
    "steamid": STEAM_USER_ID,
    "appid": 16900,
    "priority": 303
}]
WISHLIST = [
    {
        'steamid': STEAM_USER_ID,
        "appid": 16900,
        "priority": 303
    },
    {
        'steamid': STEAM_USER_ID,
        "appid": 34010,
        "priority": 424
    }
]
DB_WISHLIST_PROCESSED = [
    {'steamid': '76561198041511379', 'appid': 362490, 'priority': 253}, 
    {'steamid': '76561198041511379', 'appid': 362680, 'priority': 132}
]


# ------------------------
# ------  LIBRARY  -------
# ------------------------
CORRECT_LIBRARY_RESPONSE = {
    "response": {
        "game_count": 469,
        "games": [
            {
                "appid": 4000,
                "playtime_forever": 282,
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "playtime_deck_forever": 0,
                "rtime_last_played": 1547887933,
                "playtime_disconnected": 0
            }
        ]
    }
}
EMPTY_LIBRARY_RESPONSE = {
    "response": {
        "games": [{}]
    }
}
DB_LIBRARY_RESPONSE = [
    ('76561198041511379',  362490, 253, 200),
    ('76561198041511379',  362680, 132, 50) 
]

# PROCESS DATA
CORRECT_LIBRARY_PROCESSED = [
    {
        'steamid': STEAM_USER_ID,
        "appid": 4000,
        "playtime_minutes": 282
    }
]
DB_LIBRARY_PROCESSED = [
    {'steamid': STEAM_USER_ID, 'appid': 362490, 'playtime_minutes': 253, "user_paid_price": 200},
    {'steamid': STEAM_USER_ID, 'appid': 362680, 'playtime_minutes': 132, "user_paid_price": 50}
]



# ------------------------
# -------  GAMES  --------
# ------------------------
CORRECT_GAME_RESPONSE = {
    "1144200": {
        "success": True,
        "data": {
            "type": "game",
            "name": "Ready or Not",
            "steam_appid": 1144200,
            "required_age": 0,
            "is_free": False,
            "controller_support": "full",
            "dlc": [
                3015760,
                3089910,
                3174120
            ],
            "detailed_description": "<p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/Discord-Banner-Rifle-Shot-Render-v1.2.gif?t=1744212321\" /><br>Be sure to join the Ready or Not Discord server to keep up with the latest updates, find recruits for your squad, and have a good time!</p><h2 class=\"bb_tag\">Los Sueños</h2><p class=\"bb_paragraph\">- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.” </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">In response to the burgeoning violent crime wave inundating Los Sueños, Chief Álvarez of the LSPD has enlisted the stalwart support of David ‘Judge’ Beaumont as the Commander of the LSPD SWAT team. Shortly following this announcement, the LSPD has also confirmed active recruitment for additional talent to join this specialized tactical police unit with the mission of bringing peace back to the city. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">“This assignment is not for the faint of heart,” comments Commander Beaumont, “Extremists, crooked politicians, countless weapons, human trafficking, and illicit drugs and pornography… the world of policing in Los Sueños is fraught with real and harsh realities, realities that the everyday person isn’t necessarily confronted with. These are realities that you will need to navigate with your team within the proper bounds of the law or face the consequences and make matters worse.” </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">The Los Sueños Policed Department has officially posted new details on Commander “Judge” Beaumont’s updated assignment with the LSPD SWAT team: </p><p class=\"bb_paragraph\"></p><h2 class=\"bb_tag\">New Expectations:</h2><p class=\"bb_paragraph\">Whether this is your first time in Los Sueños or not, the city has changed and so too have the tools and methods with which we conduct our work. The haunts you might have seen or heard about are re-imagined, and so have the angles with which we approach each call. Furthermore, we’ve received reports that identify at least 4 new high-risk police districts which we suspect may require future tactical intervention, plus at least 4 existing high-risk districts that underwent massive upheavals. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/sp_coop.png?t=1744212321\" /></p><h2 class=\"bb_tag\">Take Command:</h2><p class=\"bb_paragraph\">The role of the Commander of the LSPD SWAT is to compose their team from a large roster with unique talents, give tactical orders, meticulously plan, and carry out missions. Commanders are obligated to conduct each mission with integrity and look after their team’s mental and physical health. Officers with unaddressed deteriorating mental status may be unable to properly perform their duties or even feel compelled to quit the force. Incapacitated officers may be temporarily unavailable for missions, with the tragic prospect of death leading to a permanent loss. For SWAT Commanders in unusual circumstances based on individual choices they opt for, deadly mistakes may lead to their own permanent fatality. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/Image_05.png?t=1744212321\" /></p><h2 class=\"bb_tag\">SWAT Team Quality Enhancement: </h2><p class=\"bb_paragraph\">Much anticipated improved SWAT training procedures, tactics, and experience in the LSPD has led to an overall increase in the quality and quantity of officers in our roster. Expanded tactical versatility allows our officers to take on any challenge with renewed confidence, blending coordination and independence seamlessly. There is also additional basic training now available to SWAT members to keep foundational knowledge and muscle memory in top shape. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/authentic3.png?t=1744212321\" /></p><h2 class=\"bb_tag\">Equipment and customization:</h2><p class=\"bb_paragraph\">We have access to the best weapons and equipment that the LSPD can offer to fulfill our exceptionally dangerous role, including many new acquisitions. However, customization isn’t limited to the equipment we use. Through close-knit comradery while performing remarkable actions alongside the team, you’ll earn the clothes you wear, the patches on your sleeves, the artwork that may adorn your skin, and potentially even the timepiece on your wrist. Lastly, we have overhauled our headquarters' training facilities to better test our loadouts before heading out on call.</p>",
            "about_the_game": "<p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/Discord-Banner-Rifle-Shot-Render-v1.2.gif?t=1744212321\" /><br>Be sure to join the Ready or Not Discord server to keep up with the latest updates, find recruits for your squad, and have a good time!</p><h2 class=\"bb_tag\">Los Sueños</h2><p class=\"bb_paragraph\">- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.” </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">In response to the burgeoning violent crime wave inundating Los Sueños, Chief Álvarez of the LSPD has enlisted the stalwart support of David ‘Judge’ Beaumont as the Commander of the LSPD SWAT team. Shortly following this announcement, the LSPD has also confirmed active recruitment for additional talent to join this specialized tactical police unit with the mission of bringing peace back to the city. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">“This assignment is not for the faint of heart,” comments Commander Beaumont, “Extremists, crooked politicians, countless weapons, human trafficking, and illicit drugs and pornography… the world of policing in Los Sueños is fraught with real and harsh realities, realities that the everyday person isn’t necessarily confronted with. These are realities that you will need to navigate with your team within the proper bounds of the law or face the consequences and make matters worse.” </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\">The Los Sueños Policed Department has officially posted new details on Commander “Judge” Beaumont’s updated assignment with the LSPD SWAT team: </p><p class=\"bb_paragraph\"></p><h2 class=\"bb_tag\">New Expectations:</h2><p class=\"bb_paragraph\">Whether this is your first time in Los Sueños or not, the city has changed and so too have the tools and methods with which we conduct our work. The haunts you might have seen or heard about are re-imagined, and so have the angles with which we approach each call. Furthermore, we’ve received reports that identify at least 4 new high-risk police districts which we suspect may require future tactical intervention, plus at least 4 existing high-risk districts that underwent massive upheavals. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/sp_coop.png?t=1744212321\" /></p><h2 class=\"bb_tag\">Take Command:</h2><p class=\"bb_paragraph\">The role of the Commander of the LSPD SWAT is to compose their team from a large roster with unique talents, give tactical orders, meticulously plan, and carry out missions. Commanders are obligated to conduct each mission with integrity and look after their team’s mental and physical health. Officers with unaddressed deteriorating mental status may be unable to properly perform their duties or even feel compelled to quit the force. Incapacitated officers may be temporarily unavailable for missions, with the tragic prospect of death leading to a permanent loss. For SWAT Commanders in unusual circumstances based on individual choices they opt for, deadly mistakes may lead to their own permanent fatality. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/Image_05.png?t=1744212321\" /></p><h2 class=\"bb_tag\">SWAT Team Quality Enhancement:</h2><p class=\"bb_paragraph\">Much anticipated improved SWAT training procedures, tactics, and experience in the LSPD has led to an overall increase in the quality and quantity of officers in our roster. Expanded tactical versatility allows our officers to take on any challenge with renewed confidence, blending coordination and independence seamlessly. There is also additional basic training now available to SWAT members to keep foundational knowledge and muscle memory in top shape. </p><p class=\"bb_paragraph\"></p><p class=\"bb_paragraph\"><img class=\"bb_img\" src=\"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/extras/authentic3.png?t=1744212321\" /></p><h2 class=\"bb_tag\">Equipment and customization:</h2><p class=\"bb_paragraph\">We have access to the best weapons and equipment that the LSPD can offer to fulfill our exceptionally dangerous role, including many new acquisitions. However, customization isn’t limited to the equipment we use. Through close-knit comradery while performing remarkable actions alongside the team, you’ll earn the clothes you wear, the patches on your sleeves, the artwork that may adorn your skin, and potentially even the timepiece on your wrist. Lastly, we have overhauled our headquarters' training facilities to better test our loadouts before heading out on call.</p>",
            "short_description": "Ready or Not is an intense, tactical, first-person shooter that depicts a modern-day world in which SWAT police units are called to defuse hostile and confronting situations.",
            "supported_languages": "English<strong>*</strong>, French, German, Korean, Simplified Chinese, Italian, Spanish - Spain, Japanese, Polish, Portuguese - Portugal, Turkish<br><strong>*</strong>languages with full audio support",
            "header_image": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/header.jpg?t=1744212321",
            "capsule_image": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/capsule_231x87.jpg?t=1744212321",
            "capsule_imagev5": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/capsule_184x69.jpg?t=1744212321",
            "website": "https://voidinteractive.net",
            "pc_requirements": {
                "minimum": "<strong>Minimum:</strong><br><ul class=\"bb_ul\"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10, Windows 11<br></li><li><strong>Processor:</strong> Intel Core i5-4430 / AMD FX-6300<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> NVIDIA GeForce GTX 960 2GB / AMD Radeon R7 370 2GB<br></li><li><strong>DirectX:</strong> Version 11<br></li><li><strong>Storage:</strong> 60 GB available space</li></ul>",
                "recommended": "<strong>Recommended:</strong><br><ul class=\"bb_ul\"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> 64-bit Windows 10, 64-bit Windows 11<br></li><li><strong>Processor:</strong> AMD Ryzen 5-1600 / Intel Core i5-7600K<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> Nvidia GTX 1060 6GB or better<br></li><li><strong>DirectX:</strong> Version 11<br></li><li><strong>Storage:</strong> 60 GB available space</li></ul>"
            },
            "mac_requirements": {
                "minimum": "<strong>Minimum:</strong><br><ul class=\"bb_ul\"></ul>",
                "recommended": "<strong>Recommended:</strong><br><ul class=\"bb_ul\"></ul>"
            },
            "linux_requirements": {
                "minimum": "<strong>Minimum:</strong><br><ul class=\"bb_ul\"></ul>",
                "recommended": "<strong>Recommended:</strong><br><ul class=\"bb_ul\"></ul>"
            },
            "legal_notice": "Ready or Not © VOID Interactive Ltd",
            "developers": [
                "VOID Interactive"
            ],
            "publishers": [
                "VOID Interactive"
            ],
            "price_overview": {
                "currency": "USD",
                "initial": 4999,
                "final": 2499,
                "discount_percent": 50,
                "initial_formatted": "$49.99",
                "final_formatted": "$24.99"
            },
            "packages": [
                389471
            ],
            "package_groups": [
                {
                    "name": "default",
                    "title": "Buy Ready or Not",
                    "description": "",
                    "selection_text": "Select a purchase option",
                    "save_text": "",
                    "display_type": 0,
                    "is_recurring_subscription": "false",
                    "subs": [
                        {
                            "packageid": 389471,
                            "percent_savings_text": "-50% ",
                            "percent_savings": 0,
                            "option_text": "Ready Or Not - <span class=\"discount_original_price\">$49.99</span> $24.99",
                            "option_description": "",
                            "can_get_free_license": "0",
                            "is_free_license": False,
                            "price_in_cents_with_discount": 2499
                        }
                    ]
                }
            ],
            "platforms": {
                "windows": True,
                "mac": False,
                "linux": False
            },
            "categories": [
                {
                    "id": 2,
                    "description": "Single-player"
                },
                {
                    "id": 1,
                    "description": "Multi-player"
                },
                {
                    "id": 9,
                    "description": "Co-op"
                },
                {
                    "id": 38,
                    "description": "Online Co-op"
                },
                {
                    "id": 22,
                    "description": "Steam Achievements"
                },
                {
                    "id": 28,
                    "description": "Full controller support"
                },
                {
                    "id": 23,
                    "description": "Steam Cloud"
                }
            ],
            "genres": [
                {
                    "id": "1",
                    "description": "Action"
                },
                {
                    "id": "25",
                    "description": "Adventure"
                },
                {
                    "id": "23",
                    "description": "Indie"
                }
            ],
            "screenshots": [
                {
                    "id": 0,
                    "path_thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/ss_beb0f53b0db7e85ba9e7cf99e8511e60156f19a4.600x338.jpg?t=1744212321",
                    "path_full": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/ss_beb0f53b0db7e85ba9e7cf99e8511e60156f19a4.1920x1080.jpg?t=1744212321"
                }
            ],
            "movies": [
                {
                    "id": 256987629,
                    "name": "Are you Ready?",
                    "thumbnail": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/256987629/movie.293x165.jpg?t=1702510541",
                    "webm": {
                        "480": "http://video.akamai.steamstatic.com/store_trailers/256987629/movie480_vp9.webm?t=1702510541",
                        "max": "http://video.akamai.steamstatic.com/store_trailers/256987629/movie_max_vp9.webm?t=1702510541"
                    },
                    "mp4": {
                        "480": "http://video.akamai.steamstatic.com/store_trailers/256987629/movie480.mp4?t=1702510541",
                        "max": "http://video.akamai.steamstatic.com/store_trailers/256987629/movie_max.mp4?t=1702510541"
                    },
                    "highlight": True
                }
            ],
            "recommendations": {
                "total": 180814
            },
            "achievements": {
                "total": 33,
                "highlighted": [
                    {
                        "name": "First Arrest",
                        "path": "https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/1144200/0003116331dc9fa164a519f692d30d12fec3dde9.jpg"
                    }
                ]
            },
            "release_date": {
                "coming_soon": False,
                "date": "Dec 13, 2023"
            },
            "support_info": {
                "url": "https://voidinteractive.net/",
                "email": "support@voidinteractive.net"
            },
            "background": "https://store.akamai.steamstatic.com/images/storepagebackground/app/1144200?t=1744212321",
            "background_raw": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/page_bg_raw.jpg?t=1744212321",
            "content_descriptors": {
                "ids": [
                    1,
                    2,
                    5
                ],
                "notes": "Given the graphic nature of the game and the gritty realism it portrays, the game is for mature audiences. We will also strongly recommend that people who have experienced personal traumatic events from criminal violence, hostage situations or terrorism refrain from playing. At its core, the game honors the work of dedicated law enforcement officers across the world and in no way intends on glorifying cowardly criminal acts."
            },
            "ratings": {
                "dejus": {
                    "rating": "18",
                    "descriptors": "Violência Extrema\r\nDrogas ilícitas\r\nConteúdo sexual",
                    "use_age_gate": "true",
                    "required_age": "18"
                },
                "steam_germany": {
                    "rating_generated": "1",
                    "rating": "18",
                    "required_age": "18",
                    "banned": "0",
                    "use_age_gate": "0",
                    "descriptors": "Drastische Gewalt"
                }
            }
        }
    }
}
GAME_INVALID_APPID_RESPONSE = {
    "1144513": {
        "success": True,
        "data": {}
    }
}
GAME_SUCCESS_FALSE_RESPONSE = {
    "1144513": {
        "success": False,
        "data": {}
    }
}
GAME_EMPTY_DATA_RESPONSE = {
    "1144513": {
        "success": False,
        "data": {}
    }
}
# PROCESS DATA
CORRECT_GAME_PROCESSED = {
    "appid": 1144200,
    "game_type": "game",
    "game_name": "Ready or Not",
    "is_free": False,
    "detailed_description": """Be sure to join the Ready or Not Discord server to keep up with the latest updates, find recruits for your squad, and have a good time!Los Sueños- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home. It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.” In response to the burgeoning violent crime wave inundating Los Sueños, Chief Álvarez of the LSPD has enlisted the stalwart support of David ‘Judge’ Beaumont as the Commander of the LSPD SWAT team. Shortly following this announcement, the LSPD has also confirmed active recruitment for additional talent to join this specialized tactical police unit with the mission of bringing peace back to the city. “This assignment is not for the faint of heart,” comments Commander Beaumont, “Extremists, crooked politicians, countless weapons, human trafficking, and illicit drugs and pornography… the world of policing in Los Sueños is fraught with real and harsh realities, realities that the everyday person isn’t necessarily confronted with. These are realities that you will need to navigate with your team within the proper bounds of the law or face the consequences and make matters worse.” The Los Sueños Policed Department has officially posted new details on Commander “Judge” Beaumont’s updated assignment with the LSPD SWAT team: New Expectations:Whether this is your first time in Los Sueños or not, the city has changed and so too have the tools and methods with which we conduct our work. The haunts you might have seen or heard about are re-imagined, and so have the angles with which we approach each call. Furthermore, we’ve received reports that identify at least 4 new high-risk police districts which we suspect may require future tactical intervention, plus at least 4 existing high-risk districts that underwent massive upheavals. Take Command:The role of the Commander of the LSPD SWAT is to compose their team from a large roster with unique talents, give tactical orders, meticulously plan, and carry out missions. Commanders are obligated to conduct each mission with integrity and look after their team’s mental and physical health. Officers with unaddressed deteriorating mental status may be unable to properly perform their duties or even feel compelled to quit the force. Incapacitated officers may be temporarily unavailable for missions, with the tragic prospect of death leading to a permanent loss. For SWAT Commanders in unusual circumstances based on individual choices they opt for, deadly mistakes may lead to their own permanent fatality. SWAT Team Quality Enhancement: Much anticipated improved SWAT training procedures, tactics, and experience in the LSPD has led to an overall increase in the quality and quantity of officers in our roster. Expanded tactical versatility allows our officers to take on any challenge with renewed confidence, blending coordination and independence seamlessly. There is also additional basic training now available to SWAT members to keep foundational knowledge and muscle memory in top shape. Equipment and customization:We have access to the best weapons and equipment that the LSPD can offer to fulfill our exceptionally dangerous role, including many new acquisitions. However, customization isn’t limited to the equipment we use. Through close-knit comradery while performing remarkable actions alongside the team, you’ll earn the clothes you wear, the patches on your sleeves, the artwork that may adorn your skin, and potentially even the timepiece on your wrist. Lastly, we have overhauled our headquarters' training facilities to better test our loadouts before heading out on call.""",
    "header_image": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/header.jpg?t=1744212321",
    "website": "https://voidinteractive.net",
    "recommendations": 180814,
    "release_date": "Dec 13, 2023",
    "esrb_rating": 'rp',
    "developers": [
        "VOID Interactive"
    ],
    "publishers": [
        "VOID Interactive"
    ],
    "categories": [
        {
            "id": 2,
            "description": "Single-player"
        },
        {
            "id": 1,
            "description": "Multi-player"
        },
        {
            "id": 9,
            "description": "Co-op"
        },
        {
            "id": 38,
            "description": "Online Co-op"
        },
        {
            "id": 22,
            "description": "Steam Achievements"
        },
        {
            "id": 28,
            "description": "Full controller support"
        },
        {
            "id": 23,
            "description": "Steam Cloud"
        }
    ],
    "genres": [
        {
            "id": "1",
            "description": "Action"
        },
        {
            "id": "25",
            "description": "Adventure"
        },
        {
            "id": "23",
            "description": "Indie"
        }
    ],
    "price_overview": {
        "currency": "USD",
        "price_in_cents": 4999,
        "final_formatted": "$24.99",
        "discount_percentage": 50
    },
    "metacritic": {
        "score": 0,
        "url":  ""
    }
}
DB_GAMES_RESPONSE = [
    ("game",
    "Ready or Not",
     False,
    "Be sure to join the Ready or Not Discord server to keep up with the latest updates, find recruits for your squad, and have a good time!Los Sueños- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home. It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.” In response to the burgeoning violent crime wave inundating Los Sueños, Chief Álvarez of the LSPD has enlisted the stalwart support of David ‘Judge’ Beaumont as the Commander of the LSPD SWAT team. Shortly following this announcement, the LSPD has also confirmed active recruitment for additional talent to join this specialized tactical police unit with the mission of bringing peace back to the city. “This assignment is not for the faint of heart,” comments Commander Beaumont, “Extremists, crooked politicians, countless weapons, human trafficking, and illicit drugs and pornography… the world of policing in Los Sueños is fraught with real and harsh realities, realities that the everyday person isn’t necessarily confronted with. These are realities that you will need to navigate with your team within the proper bounds of the law or face the consequences and make matters worse.” The Los Sueños Policed Department has officially posted new details on Commander “Judge” Beaumont’s updated assignment with the LSPD SWAT team: New Expectations:Whether this is your first time in Los Sueños or not, the city has changed and so too have the tools and methods with which we conduct our work. The haunts you might have seen or heard about are re-imagined, and so have the angles with which we approach each call. Furthermore, we’ve received reports that identify at least 4 new high-risk police districts which we suspect may require future tactical intervention, plus at least 4 existing high-risk districts that underwent massive upheavals. Take Command:The role of the Commander of the LSPD SWAT is to compose their team from a large roster with unique talents, give tactical orders, meticulously plan, and carry out missions. Commanders are obligated to conduct each mission with integrity and look after their team’s mental and physical health. Officers with unaddressed deteriorating mental status may be unable to properly perform their duties or even feel compelled to quit the force. Incapacitated officers may be temporarily unavailable for missions, with the tragic prospect of death leading to a permanent loss. For SWAT Commanders in unusual circumstances based on individual choices they opt for, deadly mistakes may lead to their own permanent fatality. SWAT Team Quality Enhancement: Much anticipated improved SWAT training procedures, tactics, and experience in the LSPD has led to an overall increase in the quality and quantity of officers in our roster. Expanded tactical versatility allows our officers to take on any challenge with renewed confidence, blending coordination and independence seamlessly. There is also additional basic training now available to SWAT members to keep foundational knowledge and muscle memory in top shape. Equipment and customization:We have access to the best weapons and equipment that the LSPD can offer to fulfill our exceptionally dangerous role, including many new acquisitions. However, customization isn’t limited to the equipment we use. Through close-knit comradery while performing remarkable actions alongside the team, you’ll earn the clothes you wear, the patches on your sleeves, the artwork that may adorn your skin, and potentially even the timepiece on your wrist. Lastly, we have overhauled our headquarters' training facilities to better test our loadouts before heading out on call.",
     "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/header.jpg?t=1744212321",
     "https://voidinteractive.net",
     180814,
    "Dec 13, 2023",
    'rp')
 ]
CORRECT_GAMES_PROCESSED = {
    "game_type": "game",
    "game_name": "Ready or Not",
    "is_free": False,
    "detailed_description": """Be sure to join the Ready or Not Discord server to keep up with the latest updates, find recruits for your squad, and have a good time!Los Sueños- The LSPD reports a massive upsurge in violent crime across the greater Los Sueños area. Special Weapons and Tactics (SWAT) teams have been dispatched to respond to various scenes involving high-risk hostage situations, active bomb threats, barricaded suspects, and other criminal activities. Citizens are being advised to practice caution when traveling the city or to stay at home. It has been noted that while Los Sueños is still seen as a city where riches can be found, for many more the finer things in life are becoming less and less obtainable. “The city is sprawling with cramped high-rise apartments and decaying affordable housing, which has been exploited by the criminal underground like a malevolent parasite,” states Chief Galo Álvarez. “In a city where people are just trying to survive, lawful action from the LSPD and the LSPD SWAT team remains an integral force preventing the stretched thin social fabric in this city from snapping under this chaotic strain.” In response to the burgeoning violent crime wave inundating Los Sueños, Chief Álvarez of the LSPD has enlisted the stalwart support of David ‘Judge’ Beaumont as the Commander of the LSPD SWAT team. Shortly following this announcement, the LSPD has also confirmed active recruitment for additional talent to join this specialized tactical police unit with the mission of bringing peace back to the city. “This assignment is not for the faint of heart,” comments Commander Beaumont, “Extremists, crooked politicians, countless weapons, human trafficking, and illicit drugs and pornography… the world of policing in Los Sueños is fraught with real and harsh realities, realities that the everyday person isn’t necessarily confronted with. These are realities that you will need to navigate with your team within the proper bounds of the law or face the consequences and make matters worse.” The Los Sueños Policed Department has officially posted new details on Commander “Judge” Beaumont’s updated assignment with the LSPD SWAT team: New Expectations:Whether this is your first time in Los Sueños or not, the city has changed and so too have the tools and methods with which we conduct our work. The haunts you might have seen or heard about are re-imagined, and so have the angles with which we approach each call. Furthermore, we’ve received reports that identify at least 4 new high-risk police districts which we suspect may require future tactical intervention, plus at least 4 existing high-risk districts that underwent massive upheavals. Take Command:The role of the Commander of the LSPD SWAT is to compose their team from a large roster with unique talents, give tactical orders, meticulously plan, and carry out missions. Commanders are obligated to conduct each mission with integrity and look after their team’s mental and physical health. Officers with unaddressed deteriorating mental status may be unable to properly perform their duties or even feel compelled to quit the force. Incapacitated officers may be temporarily unavailable for missions, with the tragic prospect of death leading to a permanent loss. For SWAT Commanders in unusual circumstances based on individual choices they opt for, deadly mistakes may lead to their own permanent fatality. SWAT Team Quality Enhancement: Much anticipated improved SWAT training procedures, tactics, and experience in the LSPD has led to an overall increase in the quality and quantity of officers in our roster. Expanded tactical versatility allows our officers to take on any challenge with renewed confidence, blending coordination and independence seamlessly. There is also additional basic training now available to SWAT members to keep foundational knowledge and muscle memory in top shape. Equipment and customization:We have access to the best weapons and equipment that the LSPD can offer to fulfill our exceptionally dangerous role, including many new acquisitions. However, customization isn’t limited to the equipment we use. Through close-knit comradery while performing remarkable actions alongside the team, you’ll earn the clothes you wear, the patches on your sleeves, the artwork that may adorn your skin, and potentially even the timepiece on your wrist. Lastly, we have overhauled our headquarters' training facilities to better test our loadouts before heading out on call.""",
    "header_image": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1144200/header.jpg?t=1744212321",
    "website": "https://voidinteractive.net",
    "recommendations": 180814,
    "release_date": "Dec 13, 2023",
    "esrb_rating": 'rp'
}
DB_DEVELOPERS_RESPONSE = [
    ("VOID Interactive",)
]
CORRECT_DEVELOPERS_PROCESSED = [
    {
        "developer_name": "VOID Interactive"
    }
]
CORRECT_ADD_DEVELOPERS_PROCESSED = [
    {
        "appid": 1144200,
        "developer_name": "VOID Interactive"
    }
]
DB_PUBLISHERS_RESPONSE = [
    ("VOID Interactive",)
]
CORRECT_PUBLISHERS_PROCESSED = [
    {
        "publisher_name": "VOID Interactive"
    }
]
CORRECT_ADD_PUBLISHERS_PROCESSED = [
    {
        "appid": 1144200,
        "publisher_name": "VOID Interactive"
    }
]
DB_CATEGORIES_RESPONSE = [
    ("Single-player",),
    ("Multi-player",),
    ("Co-op",),
    ("Online Co-op",),
    ("Steam Achievements",),
    ("Full controller support",),
    ("Steam Cloud",)
]
CORRECT_CATEGORIES_PROCESSED = [
    {
        "category_name": "Single-player"
    },
    {
        "category_name": "Multi-player"
    },
    {
        "category_name": "Co-op"
    },
    {
        "category_name": "Online Co-op"
    },
    {
        "category_name": "Steam Achievements"
    },
    {
        "category_name": "Full controller support"
    },
    {
        "category_name": "Steam Cloud"
    }
]
CORRECT_ADD_CATEGORIES_PROCESSED = [
    {
        "appid": 1144200,
        "category_name": "Single-player"
    },
    {
        "appid": 1144200,
        "category_name": "Multi-player"
    },
    {
        "appid": 1144200,
        "category_name": "Co-op"
    },
    {
        "appid": 1144200,
        "category_name": "Online Co-op"
    },
    {
        "appid": 1144200,
        "category_name": "Steam Achievements"
    },
    {
        "appid": 1144200,
        "category_name": "Full controller support"
    },
    {
        "appid": 1144200,
        "category_name": "Steam Cloud"
    }
]
DB_GENRES_RESPONSE = [
    ("Action",),
    ("Adventure",),
    ("Indie",)
]
CORRECT_GENRES_PROCESSED = [
    {
        "genre_name": "Action"
    },
    {
        "genre_name": "Adventure"
    },
    {
        "genre_name": "Indie"
    }
]
CORRECT_ADD_GENRES_PROCESSED = [
    {
        "appid": 1144200,
        "genre_name": "Action"
    },
    {
        "appid": 1144200,
        "genre_name": "Adventure"
    },
    {
        "appid": 1144200,
        "genre_name": "Indie"
    }
]
DB_PRICES_RESPONSE = [
    ("USD", 4999, "$24.99", 50)
]
CORRECT_PRICES_PROCESSED = {
        "currency": "USD",
        "price_in_cents": 4999,
        "final_formatted": "$24.99",
        "discount_percentage": 50
}
CORRECT_ADD_PRICES_PROCESSED = [
     {
        "appid": 1144200,
        "currency": "USD",
        "price_in_cents": 4999,
        "final_formatted": "$24.99",
        "discount_percentage": 50
    }
]
DB_META_RESPONSE = [
    (0, "")
]
CORRECT_META_PROCESSED = {
        "score": 0,
        "url": "",
}
CORRECT_ADD_META_PROCESSED = [
     {
        "appid": 1144200,
        "score": 0,
        "url": "",
    }
]


# ------------------------
# -------  PRICES  -------
# ------------------------
CORRECT_USER_PRICES = [
    {
      "game_name": "Unboxing the Cryptic Killer",
      "price": 359
    },
    {
      "game_name": "Darkwood",
      "price": 374
    },
    {
      "game_name": "INSIDE",
      "price": 199
    }
]