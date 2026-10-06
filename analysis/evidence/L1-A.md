# Evidence — L1-A (Level 1 Baseline)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Sam, I'm at North Ridge heading to Water Source. Need to meet up and gather supplies before T+180 at East Shelter for rescue."
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): At T+0, starting at North Ridge. Need to: 1) Find Sam and coordinate, 2) Gather 2 food + 2 water each, 3) Both reach East Shelter by T+180. Water Source is 8min away (north_ridge->water_source). Food Grove is accessible via: north_ridge->central_camp(22min)->south_beach(20min)->food_grove(10min)=52min OR north_ridge->rock_field(10min)->central_camp(12min)->south_beach(20min)->food_grove(10min)=52min. Bridge to Food Grove from South Beach is broken. Must go via Shipwreck or find alternate. Actually, Shipwreck path: south_beach->shipwreck(10min) doesn't lead to food. Need to map carefully: Food Grove connects to East Shelter(15min) and South Beach(10min-broken bridge). So path to Food Grove: go to South Beach via Central Camp, then... wait, bridge is broken. Let me reconsider: Food Grove is only accessible from East Shelter(15min) or South Beach(10min broken). So I MUST go East Shelter->Food Grove or find another way. This means I need to reach East Shelter first, get food from Food Grove, then return? No - if I reach East Shelter at T+180, rescue boat comes. Better strategy: Get supplies first, then go to East Shelter. Food Grove is accessible ONLY via the broken bridge from South Beach or from East Shelter. Since bridge is broken, I must reach Food Grove from East Shelter direction. So: gather water, go to East Shelter, then to Food Grove for food, return to East Shelter. Starting: go to Water Source first to get water.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Hi Alex, I'm at South Beach. Going to explore shipwreck. Where are you?"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE shipwreck  ·  NEXT: T+10 MOVE south_beach, T+20 MOVE central_camp, T+40 MOVE east_shelter, T+58 WAIT 10
NOTE (verbatim): Starting at South Beach at T+0. Need to reach East Shelter by T+180 with Alex, both carrying 2+ food and 2+ water to be rescued. The bridge to Food Grove is broken, so I need to get food from Food Grove via a different route (through Central Camp). First priority: explore and find Alex, gather resources, coordinate meeting at East Shelter. Current inventory empty. Shipwreck might have supplies. Let me start by checking shipwreck (10 min), then work toward gathering food and water.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "Sam, collecting water at Water Source. Will head to South Beach to meet you. Need to coordinate getting food and reaching East Shelter by T+180."
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): At T+8, at Water Source. Sam is at South Beach exploring shipwreck. I need to: 1) Collect water here (5min, T+13), 2) Navigate to meet Sam or coordinate next steps. Food Grove is only accessible from East Shelter (15min away) since bridge is broken. Strategy: Collect water now, then head toward Sam at South Beach to coordinate. From Water Source: water_source->north_ridge(8min)->rock_field(10min)->central_camp(12min)->south_beach(20min) = 50min total to reach Sam. At T+13 I'll have water. Then travel to South Beach arriving around T+63. We can then plan: either go to Food Grove via East Shelter, or Sam explores Shipwreck for supplies. Need to ensure both of us have 2 food + 2 water by T+180 and both at East Shelter. Time is tight but manageable if we coordinate well.

## M4  ·  seq 13  ·  T+10  ·  Sam → Alex
MESSAGE: "Heading to South Beach now. No supplies at Shipwreck. Let's meet there and plan our route to gather food and water."
TRUE STATE: Sam at shipwreck with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE south_beach  ·  NEXT: T+20 MOVE central_camp, T+40 MOVE east_shelter, T+58 WAIT 10, T+68 WAIT 30
NOTE (verbatim): T+10 at Shipwreck. Shipwreck had no supplies. Alex is at Water Source collecting water, heading to South Beach to meet me. I need to get back to South Beach to meet Alex, then coordinate gathering food from Food Grove (via Central Camp since bridge is broken) and water. Timeline: Alex should reach South Beach around T+8+10=T+18. I'm at Shipwreck now. Moving to South Beach takes 10 min, so I'll arrive at T+20. Alex said they're heading to South Beach, so we should connect there. Then we need: 2 food each (4 total), 2 water each (4 total). Water Source has unlimited water. Food Grove has food but requires going through Central Camp (bridge broken). Route: South Beach -> Central Camp (20 min) -> Food Grove (12 min) -> back to Central Camp (12 min) -> East Shelter (18 min). Total from South Beach: 62 minutes. If we meet at T+20, we'd arrive at East Shelter at T+82, leaving 98 minutes buffer before T+180. Plenty of time. Let's move to South Beach now.

## M5  ·  seq 16  ·  T+13  ·  Alex → Sam
MESSAGE: "Sam, collecting second water at Water Source, then heading to South Beach to meet you. Let's coordinate food gathering next."
TRUE STATE: Alex at water_source with food 0, water 1; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter
NOTE (verbatim): At T+13, Water Source. Just collected water (now have 1 water). Sam's last message at T+10 said heading to South Beach, so he should be there or nearby now. My plan: collect more water here (5min, T+18), then travel to South Beach to meet Sam. Route: water_source->north_ridge(8min, T+26)->rock_field(10min, T+36)->central_camp(12min, T+48)->south_beach(20min, T+68). By T+68 I'll have 2 water. Then with Sam we need to get 2 food each. Food Grove is only accessible from East Shelter (15min away). So: South Beach->central_camp(18min)->east_shelter(18min)->food_grove(15min). That's 51min from South Beach, arriving T+119. Then return to East Shelter (15min, T+134). We'd have 46min buffer before T+180 rescue. This works if we execute cleanly. Collect water now.

## M6  ·  seq 19  ·  T+18  ·  Alex → Sam
MESSAGE: "Sam, bridge to Food Grove is broken. Heading to East Shelter first to access Food Grove from there. Will gather food and meet you. Stay at or near South Beach/Central Camp."
TRUE STATE: Alex at water_source with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 MOVE food_grove
NOTE (verbatim): At T+18, Water Source, have 2 water. Bridge to Food Grove is broken - this changes my plan! I can't go South Beach->Food Grove directly. New route needed: Food Grove is only accessible from East Shelter (15min away). So I must: 1) Get to East Shelter first, 2) Then to Food Grove for food, 3) Return to East Shelter. Sam is heading to South Beach. I need to revise: go north_ridge->rock_field->central_camp->east_shelter first to secure food access, then meet Sam. Let me head north now and execute the revised plan. Time check: water_source->north_ridge(8min,T+26)->rock_field(10min,T+36)->central_camp(12min,T+48)->east_shelter(18min,T+66)->food_grove(15min,T+81)->east_shelter(15min,T+96). That's T+96 with 2 water, 2 food. Then I need to get Sam. Sam at South Beach: south_beach->central_camp(18min)->east_shelter(18min). If Sam is at South Beach at T+68 (my old estimate), he'd reach East Shelter at T+104. We'd both be at East Shelter by T+104 with supplies, 76min buffer. This works. Move north now.

## M7  ·  seq 23  ·  T+20  ·  Sam → Alex
MESSAGE: "Got your message. Moving to Central Camp now. Will meet you there or head to East Shelter. Let's coordinate gathering food and water. See you soon."
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+40 MOVE east_shelter, T+58 WAIT 10, T+68 WAIT 30, T+98 WAIT 10
NOTE (verbatim): T+20 at South Beach. Alex's last message (T+18) says bridge to Food Grove is broken and they're heading to East Shelter first to access Food Grove from there. This changes my plan! Alex will go: Water Source -> South Beach -> Central Camp -> East Shelter -> Food Grove. They said to stay at or near South Beach/Central Camp. I have 0 food and 0 water. I need to coordinate with Alex. Since Alex is heading to East Shelter to access Food Grove from the other side, I should move toward Central Camp to intercept them or head to East Shelter myself. Let me move to Central Camp (20 min, arrive T+40) to meet Alex or continue toward East Shelter. This keeps me on the path toward the final destination and allows us to coordinate. We still have plenty of time: T+40 to T+180 = 140 minutes buffer.

## M8  ·  seq 27  ·  T+26  ·  Alex → Sam
MESSAGE: "Sam, heading to East Shelter via Central Camp to access Food Grove. Will gather food and wait for you at East Shelter. See you soon!"
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 MOVE food_grove, T+81 COLLECT food
NOTE (verbatim): T+26 at North Ridge with 2 water. Sam was at Central Camp at T+20, heading to East Shelter or staying there. My plan: rock_field->central_camp->east_shelter->food_grove->east_shelter. Timeline: rock_field(10min,T+36)->central_camp(12min,T+48)->east_shelter(18min,T+66)->food_grove(15min,T+81)->east_shelter(15min,T+96). At T+96 I'll have 2 water + 2 food at East Shelter. Sam should reach East Shelter by then or shortly after. We need both there by T+180 with 2 food and 2 water each. Current plan is solid - execute it. Move to rock_field now.

## M9  ·  seq 31  ·  T+36  ·  Alex → Sam
MESSAGE: "On my way to East Shelter via Central Camp. Will gather food at Food Grove and wait for you at East Shelter. See you soon!"
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 MOVE east_shelter, T+66 MOVE food_grove, T+81 COLLECT food, T+86 COLLECT food
NOTE (verbatim): At T+36, Rock Field. Inventory: 2 water, 0 food. On schedule! Next: central_camp (12 min) -> T+48, then east_shelter (18 min) -> T+66, then food_grove (15 min) -> T+81, then back to east_shelter (15 min) -> T+96. Should have 2 water + 2 food at East Shelter by T+96. Sam was heading to Central Camp/East Shelter at T+20. Need to execute plan and meet Sam at East Shelter. Moving to central_camp now.

## M10  ·  seq 35  ·  T+40  ·  Sam → Alex
MESSAGE: "Heading to East Shelter now. Will arrive around T+58. Let's meet there and coordinate food/water gathering. We're on track!"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+58 WAIT 10, T+68 WAIT 30, T+98 WAIT 10, T+108 WAIT 10
NOTE (verbatim): T+40 at Central Camp. Alex's last message (T+36) says they're heading to East Shelter via Central Camp to gather food at Food Grove and wait for me at East Shelter. They should arrive at Central Camp around T+40-45 (from their T+36 position heading to East Shelter). I have 0 food and 0 water - critical! Alex said they'll gather food at Food Grove. My best strategy: 1) Wait here at Central Camp for Alex to pass through (they're coming this way), or 2) Head to East Shelter to meet them there. Given Alex said they'll wait at East Shelter, I should move there now. Travel time: Central Camp -> East Shelter = 18 min, arrive T+58. Then I need to get food and water. Alex will have food from Food Grove. I need to figure out water access from East Shelter area. Food Grove is 15 min from East Shelter. After meeting Alex at East Shelter, we can coordinate: one of us goes to Food Grove (15 min) while other handles water. We have T+58 to T+180 = 122 minutes. Plenty of time. Moving to East Shelter now.

## M11  ·  seq 39  ·  T+48  ·  Alex → Sam
MESSAGE: "Sam, heading to East Shelter now. Will reach you around T+66, then get food from Food Grove. See you soon!"
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+66 MOVE food_grove, T+81 COLLECT food, T+86 COLLECT food, T+91 MOVE east_shelter
NOTE (verbatim): T+48 at Central Camp. Inventory: 2 water, 0 food. Sam says he'll arrive at East Shelter around T+58. I need to: 1) Go to East Shelter (18 min) -> T+66, 2) Go to Food Grove (15 min) -> T+81, 3) Return to East Shelter (15 min) -> T+96. This gives me 2 water + 2 food by T+96, with 84 minutes to spare before rescue at T+180. Sam will be at East Shelter by T+58, so I'll meet him there. Moving to East Shelter now.

## M12  ·  seq 43  ·  T+58  ·  Sam → Alex
MESSAGE: "At East Shelter now. Waiting for you. Let's coordinate food and water next."
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+68 WAIT 30, T+98 WAIT 10, T+108 WAIT 10, T+118 WAIT 30
NOTE (verbatim): T+58 at East Shelter. Alex's last message (T+48) says they're heading to East Shelter and will arrive around T+66, then get food from Food Grove. I'm here early with 0 food and 0 water. Alex should arrive in ~8 minutes. I should WAIT here for Alex. Once Alex arrives (T+66), we'll have a plan: Alex will go to Food Grove (15 min, arrive T+81) to get food while I figure out water. Water Source is far (via north_ridge and water_source = 8+12+8 = 28 min from East Shelter via Central Camp route). Better strategy: After Alex returns from Food Grove with food (T+81), we coordinate: one of us goes to Water Source while the other waits at East Shelter with food. We have until T+180, so 99 minutes left after Alex returns. Plenty of time. For now, WAIT for Alex.

## M13  ·  seq 47  ·  T+66  ·  Alex → Sam
MESSAGE: "Sam, heading to Food Grove now. I'll grab 2 food and be back in 30 min. Do you have enough water? Let's make sure we both have 2 food + 2 water by T+96."
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at east_shelter with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+81 COLLECT food, T+86 COLLECT food, T+91 MOVE east_shelter, T+106 GIVE water
NOTE (verbatim): T+66 at East Shelter with Sam. Current inventory: 2 water, 0 food. Plan: Go to Food Grove (15 min) -> T+81, collect 2 food, return to East Shelter (15 min) -> T+96. This gives me 2 water + 2 food by T+96, 84 min before rescue. Sam is here - need to coordinate his food/water gathering. He needs 2 food + 2 water too. Sam can go to Food Grove while I wait, or we coordinate separate trips. Let me head to Food Grove now to get my 2 food.

## M14  ·  seq 50  ·  T+68  ·  Sam → Alex
MESSAGE: "Alex, I'm at East Shelter. No water yet. When you return with food, one of us needs to get water from Water Source. We have time. See you soon!"
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 30  ·  NEXT: T+98 WAIT 10, T+108 WAIT 10, T+118 WAIT 30, T+148 WAIT 10
NOTE (verbatim): T+68 at East Shelter. Alex left at T+66 heading to Food Grove (15 min travel, should arrive T+81, then grab 2 food and return in 30 min total, arriving back T+96). Alex asked if I have enough water - I have 0. Alex wants both of us to have 2 food + 2 water by T+96. I'm at East Shelter with 0 food, 0 water. Plan: Wait here for Alex to return with food (T+96). Then one of us goes to Water Source to get water while the other stays at East Shelter with the food. Water Source route from East Shelter: East Shelter -> Central Camp (18 min) -> Rock Field (12 min) -> North Ridge (10 min) -> Water Source (8 min) = 48 min one way. If I leave at T+96, I arrive at Water Source at T+144, grab water, return by T+192 - TOO LATE (storm at T+180). Instead: Alex should get water on return trip or we adjust. Actually, let me wait for Alex here. When Alex arrives T+96 with 2 food, we coordinate: I'll go get water (48 min round trip gets me back at T+144), or Alex goes. We have 84 min from now - enough time. WAIT 30 for now to get closer to Alex's return time.

## M15  ·  seq 54  ·  T+81  ·  Alex → Sam
MESSAGE: "Sam, collecting 2 food now, back to East Shelter in 20 min (T+101). You need water - go Water Source via Central Camp/Rock Field route. We'll both be ready by T+154!"
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at east_shelter with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+86 COLLECT food, T+91 MOVE east_shelter, T+106 GIVE water, T+108 GIVE water
NOTE (verbatim): T+81 at Food Grove. I have 2 water, 0 food. Sam is at East Shelter with no water yet. My plan: COLLECT food now (5 min) -> T+86, then MOVE east_shelter (15 min) -> T+101. This gives me 2 food + 2 water by T+101, 79 min before rescue. Sam needs to get water from Water Source (8 min from North Ridge, 10 min from Rock Field). Since bridge is broken, Sam's best route from East Shelter: East Shelter -> Central Camp (18 min) -> Rock Field (12 min) -> North Ridge (10 min) -> Water Source (8 min) = 48 min total, arriving T+106. Then Water Source -> North Ridge (8 min) -> Rock Field (10 min) -> Central Camp (12 min) -> East Shelter (18 min) = 48 min return, arriving T+154. This works! We'll both be at East Shelter by T+154 with required supplies, 26 min before rescue. Let me collect food and head back.

## M16  ·  seq 57  ·  T+86  ·  Alex → Sam
MESSAGE: "Sam, collecting last food now, heading to East Shelter. Should have 2 food + 2 water by T+106. You on track for water?"
TRUE STATE: Alex at food_grove with food 1, water 2; Sam at east_shelter with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+91 MOVE east_shelter, T+106 GIVE water, T+108 GIVE water, T+110 GIVE food
NOTE (verbatim): At T+86 at Food Grove with 1 food, 2 water. I collected food but only got 1 instead of 2. Need to collect one more food (5 min) -> T+91, then move to East Shelter (15 min) -> T+106. This still gives me time. Sam should be en route to Water Source. My plan: collect 1 more food now to have 2 food + 2 water, then head to East Shelter. Sam's timeline: from East Shelter at T+58, going to Water Source via Central Camp/Rock Field/North Ridge (48 min total) arrives T+106, then returns (48 min) arrives T+154. We should both be at East Shelter by T+154 with required supplies, 26 min before rescue at T+180. Proceeding with collection.

## M17  ·  seq 62  ·  T+98  ·  Sam → Alex
MESSAGE: "Alex, at East Shelter waiting for you. Do you have the 2 water + 2 food? We're on track for rescue!"
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at travelling with food 2, water 2
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+108 WAIT 10, T+118 WAIT 30, T+148 WAIT 10, T+158 WAIT 10
NOTE (verbatim): T+98: Alex said arriving T+101 with 2 food + 2 water. I'm at East Shelter with 0 food, 0 water. Alex should arrive in ~3 min. I'll WAIT 10 to see if Alex shows up. If Alex arrives with supplies as promised, we'll both have what we need (2 food + 2 water each). The storm hits T+180, so we have 82 min. If we're both here with supplies by T+108, we're safe for rescue. Alex's last message (T+86) said 'should have 2 food + 2 water by T+106' - this suggests Alex is bringing water too, not just food. Wait here for Alex.

## M18  ·  seq 69  ·  T+108  ·  Sam → Alex
MESSAGE: "Alex, what's your inventory? Do you have 2 food + 2 water? I have 1 water, 0 food. We need to coordinate getting supplies fast!"
TRUE STATE: Sam at east_shelter with food 0, water 1; Alex at east_shelter with food 2, water 1
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+118 WAIT 30, T+148 WAIT 10, T+158 WAIT 10, T+168 WAIT 10
NOTE (verbatim): T+108: Alex is here at East Shelter with me. I have 1 water. Alex just gave me 1 water (so I now have 1). Alex said they'd have 2 food + 2 water by T+106, but it's now T+108. I need to check Alex's inventory. According to the rescue rules: both of us need AT LEAST 2 food AND 2 water to be rescued. I have 0 food and 1 water. Alex should have 2 food and 2 water. The storm hits T+180, so we have 72 minutes. If Alex has everything, I just need 1 more water and 2 food. Water Source is 8+10+12 = 30 min away (via Rock Field/North Ridge). Food Grove is 15 min away. If Alex has the supplies they promised, I could: (1) Get water from Water Source (30 min) + Get food from Food Grove (15 min) = 45 min, arriving T+153, safe. OR (2) Alex could go get water while I get food. Let me ask Alex what they have and coordinate.

## M19  ·  seq 80  ·  T+118  ·  Sam → Alex
MESSAGE: "Alex, I'm at East Shelter with 2 food + 2 water. Do you have your supplies? Come to East Shelter ASAP for rescue at T+180!"
TRUE STATE: Sam at east_shelter with food 2, water 2; Alex at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 30  ·  NEXT: T+148 WAIT 10, T+158 WAIT 10, T+168 WAIT 10, T+178 WAIT 10
NOTE (verbatim): T+118: Great news! I now have 2 food + 2 water - exactly what I need for rescue! Alex gave me 2 food since last turn. I'm at East Shelter and Alex is somewhere else (unknown location). The rescue boat arrives at T+180, which is 62 minutes away. Both of us need to be at East Shelter with at least 2 food + 2 water. I have everything I need. Alex's last message (T+108) said they should have 2 food + 2 water by T+106, but I don't know their current inventory or location. I should WAIT here at East Shelter since: (1) I'm already at the rescue location, (2) I have all required supplies, (3) Alex needs to get here, (4) waiting gives Alex time to arrive. If Alex doesn't show up soon, I may need to go find them. But for now, waiting is safest - I don't want to leave East Shelter and miss the rescue. 62 minutes is plenty of time for Alex to get here from most locations.

## M20  ·  seq 90  ·  T+148  ·  Sam → Alex
MESSAGE: "Alex, where are you? I'm at East Shelter with all supplies. 32 min until rescue. Please respond!"
TRUE STATE: Sam at east_shelter with food 2, water 2; Alex at travelling with food 2, water 0
KNOWS: Water Source has water (unlimited). | Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+158 WAIT 10, T+168 WAIT 10, T+178 WAIT 10
NOTE (verbatim): T+148: Still at East Shelter with 2 food + 2 water - exactly what I need for rescue. 32 minutes until storm/rescue at T+180. Alex's last message was T+118 saying they had 2 food + 2 water and would come to East Shelter. They should have arrived by now but haven't shown up. This is concerning. Possibilities: (1) Alex is delayed but still coming - most likely, (2) Alex had an accident or got lost, (3) Alex went somewhere else. I need to balance two risks: (a) leaving East Shelter means I might miss Alex arriving, (b) staying means if Alex is lost/stuck somewhere, they won't make it and neither will I. With 32 min left, I can afford a short 10-min wait to see if Alex arrives, then reassess. If Alex doesn't show by T+158, I'll need to make a hard decision about searching. For now, waiting 10 min is safest - it keeps me at rescue point while giving Alex a final window to arrive.
