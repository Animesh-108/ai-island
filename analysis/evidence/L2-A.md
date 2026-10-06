# Evidence — L2-A (Level 2 Split Knowledge)

## M1  ·  seq 1  ·  T+0  ·  Alex → Sam
MESSAGE: "Sam, I'm at North Ridge heading to Water Source to get water. Where are you? Let's meet up soon."
TRUE STATE: Alex at north_ridge with food 0, water 0; Sam at south_beach with food 0, water 0
KNOWS: Water Source has water (unlimited). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE water_source  ·  NEXT: T+8 COLLECT water, T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field
NOTE (verbatim): T+0 at North Ridge. Need to find Sam and gather 2 food + 2 water each by T+180. Water Source is 8min away (west). Food Grove requires going through Central Camp. Strategy: 1) Get water first (8min to Water Source), 2) Find Sam and coordinate, 3) Gather food, 4) Both reach East Shelter by T+180. Bridge to Food Grove is broken so must use Central Camp route. 180 minutes is tight - need to move efficiently.

## M2  ·  seq 2  ·  T+0  ·  Sam → Alex
MESSAGE: "Hi Alex! I'm at South Beach heading to Food Grove to get food. We need 2 food and 2 water each to be rescued at East Shelter by T+180. Where are you?"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at north_ridge with food 0, water 0
KNOWS: Food Grove has food.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+10 MOVE central_camp, T+30 WAIT 10, T+40 WAIT 10, T+50 MOVE east_shelter
NOTE (verbatim): Starting at South Beach at T+0. Need to reach East Shelter by T+180 with Alex, both carrying 2+ food and 2+ water to be rescued. Food Grove is 10min away via bridge - should get food first. Then need to find water source and locate Alex. Total travel time to East Shelter from South Beach: South Beach->Food Grove (10min) + Food Grove->East Shelter (15min) = 25min minimum. Plenty of time to gather supplies and coordinate with Alex.

## M3  ·  seq 9  ·  T+8  ·  Alex → Sam
MESSAGE: "Got water source. Heading to Central Camp to meet you. Bridge broken so Food Grove requires going through Central Camp. See you soon!"
TRUE STATE: Alex at water_source with food 0, water 0; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+13 COLLECT water, T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp
NOTE (verbatim): T+8 at Water Source. Sam is at South Beach heading to Food Grove. I need to: 1) Collect water here (5min, then T+13), 2) Navigate to meet Sam or go to Food Grove, 3) Gather food together, 4) Both reach East Shelter by T+180. Bridge is broken so Sam cannot cross from South Beach to Food Grove directly. Sam will need to go South Beach -> Central Camp -> Food Grove or find another route. I should collect water now, then head back through North Ridge to Central Camp to coordinate with Sam. Time check: 172 min left. Water collection (5min) + travel to Central Camp via North Ridge (8+12+15=35min) = 40min total to reach Central Camp. That leaves 132min to gather food and reach East Shelter together. This is feasible but tight.

## M4  ·  seq 14  ·  T+10  ·  Sam → Alex
MESSAGE: "Heading to Central Camp now to meet you. See you soon!"
TRUE STATE: Sam at south_beach with food 0, water 0; Alex at water_source with food 0, water 1
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+30 WAIT 10, T+40 WAIT 10, T+50 MOVE east_shelter, T+68 MOVE food_grove
NOTE (verbatim): At T+10, South Beach. Alex got water at Water Source (T+8) and is heading to Central Camp. The bridge to Food Grove is broken, so I must go through Central Camp to reach Food Grove. My plan: MOVE central_camp (20min, arrive T+30) -> Food Grove (15min, arrive T+45) to get food -> meet Alex at Central Camp or coordinate next steps. We need 2 food + 2 water each by T+180. Time remaining: 170min. Route to East Shelter from Central Camp: 18min. Plenty of time if we coordinate well. Alex said 'see you soon' so they're heading to Central Camp now.

## M5  ·  seq 17  ·  T+13  ·  Alex → Sam
MESSAGE: "At Water Source collecting water. Heading to Central Camp via North Ridge & Rock Field. Meet you there!"
TRUE STATE: Alex at water_source with food 0, water 1; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT water  ·  NEXT: T+18 MOVE north_ridge, T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter
NOTE (verbatim): T+13 at Water Source with 1 water. Sam said at T+10 he's heading to Central Camp to meet me. I have 167 min left. My plan: collect more water here (5min, T+18), then move to North Ridge (8min, T+26), then to Central Camp (27min via West Forest route or 22min via Rock Field route). Rock Field is faster: North Ridge->Rock Field (10min, T+36) -> Central Camp (12min, T+48). Then coordinate with Sam to get food from Food Grove. We need 2 food + 2 water each. I have 1 water, need 1 more. Sam is heading to Central Camp. After meeting, we go to Food Grove together (15min from Central Camp), collect food, then to East Shelter (18min from Central Camp). Total time from T+48: Food Grove 15min + collect 5min + East Shelter 18min = 38min, arriving T+101. This leaves 79min buffer before T+180. Feasible. Collect water now.

## M6  ·  seq 20  ·  T+18  ·  Alex → Sam
MESSAGE: "Moving to North Ridge now, heading to Central Camp to meet you!"
TRUE STATE: Alex at water_source with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE north_ridge  ·  NEXT: T+26 MOVE rock_field, T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10
NOTE (verbatim): T+18 at Water Source with 2 water now. Good progress! My plan still works: Move to North Ridge (T+26), then Rock Field (T+36), then Central Camp (T+48). Sam said he's heading to Central Camp at T+10, so he should be there or nearby soon. After I reach Central Camp, we coordinate to get food from Food Grove (15min away), collect it (5min), then go to East Shelter (18min away). That puts us at East Shelter around T+101 with plenty of buffer before T+180. I have 2 water, need 2 food total (1 per person minimum, but ideally 2 each = 4 total). Let's move to North Ridge now.

## M7  ·  seq 24  ·  T+26  ·  Alex → Sam
MESSAGE: "At North Ridge heading to Rock Field now. Should reach Central Camp by T+48. Where are you?"
TRUE STATE: Alex at north_ridge with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE rock_field  ·  NEXT: T+36 MOVE central_camp, T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove
NOTE (verbatim): T+26 at North Ridge. Have 2 water, need 2 food total. Plan: Rock Field (T+36) -> Central Camp (T+48). Sam said he's heading to Central Camp at T+10, so he should arrive around T+10+travel time. If he went South Beach->Food Grove, the bridge is broken so he'd need to go through Central Camp anyway. He might be at Central Camp already or en route. Moving to Rock Field now to stay on schedule. After Central Camp, we get food from Food Grove (must go via Central Camp since bridge broken), then to East Shelter by T+101. Still on track with 79 min buffer before storm.

## M8  ·  seq 28  ·  T+30  ·  Sam → Alex
MESSAGE: "At Central Camp now. Waiting for you here. Should I go to Food Grove or wait?"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+40 WAIT 10, T+50 MOVE east_shelter, T+68 MOVE food_grove, T+83 COLLECT food
NOTE (verbatim): T+30 at Central Camp. Alex is heading to Central Camp via Rock Field, should arrive around T+48 (they said T+48 at T+26). I have 0 food, 0 water. Alex has at least 2 water. Plan: WAIT here for Alex to arrive (saves time vs moving). Once Alex arrives, we coordinate: one of us goes to Food Grove (15min from Central Camp) to get food, the other waits or gets more water. We need 2 food + 2 water each = 4 food + 4 water total. Time budget: 150min left. If Alex arrives T+48, we have 132min to: get food, get more water if needed, and reach East Shelter by T+180. Route from Central Camp to East Shelter is 18min, so we need to leave by T+162 latest. Plenty of time. WAIT 10 to stay at Central Camp and let Alex catch up.

## M9  ·  seq 32  ·  T+36  ·  Alex → Sam
MESSAGE: "On my way to Central Camp now, arriving T+48. Let's go to Food Grove together after I arrive."
TRUE STATE: Alex at rock_field with food 0, water 2; Sam at central_camp with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE central_camp  ·  NEXT: T+48 MOVE east_shelter, T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food
NOTE (verbatim): T+36 at Rock Field. Have 2 water, 0 food. Sam is at Central Camp waiting (his T+30 message). I need to reach Central Camp to meet him, then go to Food Grove for food. Rock Field to Central Camp is 12 min, so I'll arrive at T+48. Sam has been waiting since T+30, so he'll still be there. After Central Camp, we both go to Food Grove (15 min), arriving T+63. Then Central Camp to East Shelter (18 min), arriving T+81. That gives us 99 min buffer before T+180 storm. Both of us will have 2 food and 2 water for rescue. Proceeding to Central Camp now.

## M10  ·  seq 35  ·  T+40  ·  Sam → Alex
MESSAGE: "Still at Central Camp waiting. See you soon!"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+50 MOVE east_shelter, T+68 MOVE food_grove, T+83 COLLECT food, T+88 COLLECT food
NOTE (verbatim): T+40 at Central Camp. Alex said they'd arrive T+48, so about 8 minutes away. I have 0 food, 0 water. Alex has at least 2 water from Water Source. Plan unchanged: WAIT for Alex, then go to Food Grove together to get food. We need 4 food + 4 water total. Time budget: 140 min left. After Alex arrives (T+48), we go to Food Grove (15 min, arrive T+63), get food, then head to East Shelter (18 min from Central Camp, arrive T+81 if we leave T+63). Plenty of buffer. WAIT 10 to stay at Central Camp.

## M11  ·  seq 39  ·  T+48  ·  Alex → Sam
MESSAGE: "Let's go to East Shelter, then Food Grove to get food. We'll be back at East Shelter by T+96."
TRUE STATE: Alex at central_camp with food 0, water 2; Sam at central_camp with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+66 WAIT 10, T+76 MOVE food_grove, T+91 COLLECT food, T+96 MOVE east_shelter
NOTE (verbatim): T+48 at Central Camp with Sam. I have 2 water, 0 food. Sam is here. Bridge is broken so we can't cross South Beach->Food Grove. We must go Central Camp->East Shelter->Food Grove->East Shelter. Central Camp to East Shelter: 18 min (arrive T+66). East Shelter to Food Grove: 15 min (arrive T+81). Food Grove to East Shelter: 15 min (arrive T+96). That gives us 84 min buffer before T+180. Both of us need 2 food and 2 water. Sam likely has food from his journey. I need to get food at Food Grove. Let's head to East Shelter first, then Food Grove, then back to East Shelter.

## M12  ·  seq 42  ·  T+50  ·  Sam → Alex
MESSAGE: "On my way to East Shelter now! Meet you there?"
TRUE STATE: Sam at central_camp with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+68 MOVE food_grove, T+83 COLLECT food, T+88 COLLECT food, T+93 MOVE east_shelter
NOTE (verbatim): T+50: Alex just messaged at T+48 saying 'Let's go to East Shelter, then Food Grove to get food. We'll be back at East Shelter by T+96.' This is a NEW PLAN different from before. Alex wants to go to East Shelter FIRST, then Food Grove. But wait - the bridge to Food Grove is broken. Food Grove is only accessible from Central Camp (15 min) or South Beach (10 min, but bridge broken). If Alex is suggesting going to East Shelter first, maybe they want to scout it or they're confused about the route. Let me reconsider: East Shelter -> Food Grove is 15 min direct. So maybe Alex means: go to East Shelter (18 min from Central Camp, T+68), then to Food Grove (15 min, T+83), back to East Shelter (15 min, T+98). That's close to their T+96 estimate but slightly over. OR: Alex might be at a different location now. They said arriving T+48, but I don't know if they're here yet. I should MOVE to East Shelter to meet them there, or wait a bit longer. Given the message was sent at T+48 and it's now T+50, Alex might be arriving at Central Camp right now or might already be moving. The safest move: go to East Shelter to meet them there as they suggested. That's 18 min, arriving T+68. Then we can go to Food Grove together (15 min, T+83), and back to East Shelter (15 min, T+98). That gives us time to get food and be ready for the rescue at T+180. Let's go to East Shelter now.

## M13  ·  seq 46  ·  T+66  ·  Alex → Sam
MESSAGE: "At East Shelter now. Waiting for you. Should be here soon!"
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 10  ·  NEXT: T+76 MOVE food_grove, T+91 COLLECT food, T+96 MOVE east_shelter, T+111 GIVE water
NOTE (verbatim): T+66 at East Shelter. I have 2 water, 0 food. Sam said at T+50 he was heading to East Shelter, so he should arrive around T+68 (50+18=68). I'll wait here for him. Once he arrives, we go to Food Grove together (15 min, arrive T+83), get food, then return to East Shelter (15 min, arrive T+98). This gives us 82 min buffer before T+180. Both of us need 2 food and 2 water to be rescued.

## M14  ·  seq 50  ·  T+68  ·  Sam → Alex
MESSAGE: "Going to Food Grove now to get food! Meet you there or I'll collect and come back to East Shelter."
TRUE STATE: Sam at east_shelter with food 0, water 0; Alex at east_shelter with food 0, water 2
KNOWS: Food Grove has food. | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+83 COLLECT food, T+88 COLLECT food, T+93 MOVE east_shelter, T+108 WAIT 30
NOTE (verbatim): T+68: I'm at East Shelter with Alex. We have 0 food and 0 water each - we MUST get supplies before T+180. Alex suggested going to Food Grove after East Shelter. Food Grove is 15 min away (arrive T+83). We need to collect food there, then return to East Shelter (15 min, arrive T+98). That gives us 82 minutes before the storm/rescue at T+180 - plenty of time. After getting food, we still need water. Water Source is accessible but far. However, we might find water at other locations or Alex may have water already. Let's proceed with the plan: go to Food Grove now to get food.

## M15  ·  seq 53  ·  T+76  ·  Alex → Sam
MESSAGE: "Heading to Food Grove now to meet you! Let's get food and head back to East Shelter."
TRUE STATE: Alex at east_shelter with food 0, water 2; Sam at travelling with food 0, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE food_grove  ·  NEXT: T+91 COLLECT food, T+96 MOVE east_shelter, T+111 GIVE water, T+113 GIVE water
NOTE (verbatim): Sam is at Food Grove (or heading there) as of T+68. He said he'd collect food and come back to East Shelter. I'm at East Shelter with 2 water, 0 food. I need to get food. Sam might be at Food Grove now (T+76, so 8 min after his message). I should go to Food Grove to meet him, get food together, and return to East Shelter. Food Grove is 15 min away, so I'd arrive T+91. If Sam is there, we collect food and return T+106. That's 74 min buffer before T+180 - plenty of time. If he's not there yet, I'll wait or collect and return. Let's go.

## M16  ·  seq 57  ·  T+83  ·  Sam → Alex
MESSAGE: "Collecting food now at Food Grove. Will head back to East Shelter after. See you soon!"
TRUE STATE: Sam at food_grove with food 0, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 6 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+88 COLLECT food, T+93 MOVE east_shelter, T+108 WAIT 30, T+138 WAIT 10
NOTE (verbatim): T+83: I'm at Food Grove now. Alex messaged at T+76 saying they're heading to Food Grove to meet me. I need to collect food here (5 min, arrive T+88), then return to East Shelter (15 min, arrive T+103). That leaves 77 minutes before T+180 - still good time. After collecting food, I still need water. Alex said they were getting water at Water Source earlier. Once I collect food and return to East Shelter, I need to figure out the water situation. Let me collect food now.

## M17  ·  seq 60  ·  T+88  ·  Sam → Alex
MESSAGE: "Still here at Food Grove collecting food. Do you have water? Need to figure out water situation."
TRUE STATE: Sam at food_grove with food 1, water 0; Alex at travelling with food 0, water 2
KNOWS: Food Grove had 5 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+93 MOVE east_shelter, T+108 WAIT 30, T+138 WAIT 10, T+148 WAIT 10
NOTE (verbatim): T+88: Just collected food (now have 1 food total). I need 2 food and 2 water to be rescued. I only have 1 food and 0 water - this is a problem. Alex said they were heading to Food Grove to meet me at T+76. They should be here or arriving soon. I need to: 1) Collect more food here (5 min = T+93), 2) Get water somehow, 3) Return to East Shelter by T+180. If I collect food now (T+93), then move to East Shelter (T+108), I'll have 72 min left. But I still need 2 water and I don't have any. Alex was getting water at Water Source. I should collect the remaining food here first, then figure out the water situation. Let me collect food again.

## M18  ·  seq 64  ·  T+91  ·  Alex → Sam
MESSAGE: "Collecting food now. Then we head back to East Shelter together!"
TRUE STATE: Alex at food_grove with food 0, water 2; Sam at food_grove with food 2, water 0
KNOWS: Water Source has water (unlimited) (you were last there at T+18). | Food Grove had 4 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: COLLECT food  ·  NEXT: T+96 MOVE east_shelter, T+111 GIVE water, T+113 GIVE water, T+115 WAIT 30
NOTE (verbatim): T+91: I'm at Food Grove with Sam. He's been collecting food. I have 2 water, 0 food. Sam asked about water situation at T+88. I need to: 1) Collect food (5 min, T+96), 2) Give Sam water if needed (2 min, T+98), 3) Return to East Shelter (15 min, T+113). That gives 67 min buffer before T+180 - safe. Sam said he's collecting food, so I should collect too to ensure we both have 2 food. Let me collect food now.

## M19  ·  seq 67  ·  T+93  ·  Sam → Alex
MESSAGE: "Alex, do you have water? I have 2 food but 0 water. Moving to East Shelter now!"
TRUE STATE: Sam at food_grove with food 2, water 0; Alex at food_grove with food 1, water 2
KNOWS: Food Grove had 3 food left (you are here now). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: MOVE east_shelter  ·  NEXT: T+108 WAIT 30, T+138 WAIT 10, T+148 WAIT 10, T+158 WAIT 10
NOTE (verbatim): T+93: Alex is here at Food Grove with me. I have 2 food and 0 water. Alex just said they're collecting food. I need 2 food and 2 water to be rescued. CRITICAL PROBLEM: I have 0 water and no way to get it now. Water Source is too far away (would take 8+12+10+12+18=60 min just to get there from Food Grove via north route, then back 60 min = 120 min total, arriving T+213 which is AFTER rescue at T+180). The bridge is broken so can't go south. I'm stuck without water. Alex might have water - I should ask them about their water inventory before we move. We need to leave soon to reach East Shelter by T+180. Current plan: 1) Ask Alex if they have water, 2) Move to East Shelter now (15 min = T+108), 3) Hope Alex has water or figure out alternative. We'll have 72 minutes at East Shelter to spare. Let's go.

## M20  ·  seq 73  ·  T+108  ·  Sam → Alex
MESSAGE: "At East Shelter now. Do you have water? Please tell me your inventory!"
TRUE STATE: Sam at east_shelter with food 2, water 0; Alex at travelling with food 1, water 2
KNOWS: Food Grove had 3 food left (you were last there at T+93). | The bridge between South Beach and Food Grove is broken. It cannot be crossed.
ACTION THIS TURN: WAIT 30  ·  NEXT: T+138 WAIT 10, T+148 WAIT 10, T+158 WAIT 10, T+168 WAIT 10
NOTE (verbatim): T+108: I'm at East Shelter with 2 food and 0 water. Alex hasn't responded to my water question. I'm in critical danger - I need 2 water to be rescued but have none. Alex said they were collecting food at Food Grove at T+91. They should be heading back to East Shelter soon. I have 72 minutes until rescue at T+180. My last message asked if they have water. I need to wait here for Alex to arrive - they said they'd head back to East Shelter together. If Alex has water, we can both be rescued. If not, I'm doomed. Best option: WAIT here and hope Alex arrives with water. I'll wait 30 min (until T+138) to give them time to collect food and travel back. That still leaves 42 min buffer before T+180.
