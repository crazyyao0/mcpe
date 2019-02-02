# Preparing terrain
fill ~-10 ~ ~ ~10 ~40 ~-20 air 0 replace
fill ~-10 ~-1 ~ ~10 ~-1 ~-20 grass 0 replace
# fill ~-10 ~-6 ~ ~10 ~-2 ~-20 stone 0 replace
# Building path
fill ~-1 ~-1 ~ ~1 ~-1 ~-4 gravel 0 replace
# Building Structure
fill ~-5 ~-1 ~-5 ~5 ~4 ~-12 planks 0 hollow
fill ~-5 ~ ~-5 ~-5 ~3 ~-5 log 0 replace
fill ~-5 ~ ~-12 ~-5 ~3 ~-12 log 0 replace
fill ~5 ~ ~-5 ~5 ~3 ~-5 log 0 replace
fill ~5 ~ ~-12 ~5 ~3 ~-12 log 0 replace
# Building basemen
fill ~-5 ~-5 ~-5 ~5 ~-1 ~-12 cobblestone 0 hollow
# Building roof
fill ~-5 ~4 ~-5 ~5 ~4 ~-12 stone_slab 0 replace
setblock ~-5 ~4 ~-5 cobblestone 0
setblock ~-5 ~4 ~-12 cobblestone 0
setblock ~5 ~4 ~-5 cobblestone 0
setblock ~5 ~4 ~-12 cobblestone 0
# making door hole
fill ~ ~ ~-5 ~ ~1 ~-5 air 0 replace
# making ladder
fill ~ ~-4 ~-11 ~ ~5 ~-11 cobblestone 0 replace
fill ~ ~-4 ~-10 ~ ~5 ~-10 ladder 3 replace
# Front windows
fill ~-4 ~1 ~-5 ~-2 ~2 ~-5 glass_pane
fill ~4 ~1 ~-5 ~2 ~2 ~-5 glass_pane
# left side windows
fill ~-5 ~1 ~-7 ~-5 ~2 ~-7 glass_pane
fill ~-5 ~1 ~-10 ~-5 ~2 ~-10 glass_pane
# right side windows
fill ~5 ~1 ~-7 ~5 ~2 ~-7 glass_pane
fill ~5 ~1 ~-10 ~5 ~2 ~-10 glass_pane
# Front left flower box  
fill ~-4 ~ ~-4 ~-2 ~ ~-4 grass 0 replace
fill ~-4 ~1 ~-4 ~-2 ~1 ~-4 red_flower 0 replace
fill ~-4 ~ ~-3 ~-2 ~ ~-3 trapdoor 5 replace
setblock ~-5 ~ ~-4 trapdoor 6 replace
setblock ~-1 ~ ~-4 trapdoor 7 replace
# Front right flower box
fill ~2 ~ ~-4 ~4 ~ ~-4 grass 0 replace
fill ~2 ~1 ~-4 ~4 ~1 ~-4 red_flower 1 replace
fill ~2 ~ ~-3 ~4 ~ ~-3 trapdoor 5 replace
setblock ~1 ~ ~-4 trapdoor 6 replace
setblock ~5 ~ ~-4 trapdoor 7 replace
# placing torchs
setblock ~ ~2 ~-6 torch 4
setblock ~ ~-2 ~-6 torch 4
setblock ~-5 ~5 ~-5 torch 0
setblock ~-5 ~5 ~-12 torch 0
setblock ~5 ~5 ~-5 torch 0
setblock ~5 ~5 ~-12 torch 0
# Placing furniture
setblock ~-4 ~ ~-6 chest 5 replace
setblock ~-4 ~ ~-8 chest 5 replace
setblock ~-4 ~ ~-9 chest 5 replace
setblock ~-4 ~ ~-11 chest 5 replace
setblock ~4 ~ ~-6 dark_oak_stairs 4 replace
setblock ~4 ~ ~-7 crafting_table 4 replace
setblock ~4 ~ ~-8 dark_oak_stairs 4 replace
setblock ~4 ~ ~-9 dark_oak_stairs 4 replace
setblock ~4 ~ ~-10 cauldron 0 replace
setblock ~4 ~ ~-11 dark_oak_stairs 4 replace
fill ~-1 ~ ~-11 ~-1 ~1 ~-11 furnace 3 replace
fill ~1 ~ ~-11 ~1 ~1 ~-11 furnace 3 replace
fill ~-4 ~-4 ~-6 ~-4 ~-3 ~-6 coal_block 0 replace
setblock ~-4 ~-4 ~-7 coal_block 0 replace
setblock ~-3 ~-4 ~-6 coal_block 0 replace
setblock ~-3 ~-4 ~-8 coal_block 0 replace
fill ~4 ~-4 ~-6 ~4 ~-3 ~-6 log 0 replace
setblock ~4 ~-4 ~-7 log 0 replace
setblock ~3 ~-4 ~-6 log 0 replace
setblock ~4 ~-4 ~-9 log 0 replace