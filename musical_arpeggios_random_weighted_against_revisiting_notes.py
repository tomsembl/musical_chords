import pygame.midi, time, random
from win32com.client import Dispatch



BPM = 160
SECONDS_PER_BEAT = 60.0 / BPM
SIXTEENTH_NOTE = SECONDS_PER_BEAT / 4

CHORDS = {
    'major': (4, 3, 5),
    'major_7th': (4, 3, 4, 1),
    'major_♭7th': (4, 3, 3, 2),
    'major_6th': (4, 3, 2, 3),
    'minor': (3, 4, 5),
    'minor_add4': (3, 2, 2, 5),  
    'minor_7th': (3, 4, 3, 2),
    'minor_6th': (3, 4, 2, 3),
    'diminished': (3, 3, 6),
    'diminished_7th': (3, 3, 3, 3),  
    'augmented': (4, 4, 4),
    'major_add2': (2, 2, 3, 5),  
    'major_9th': (2, 2, 3, 4, 1),  
    'major_9th_♭7': (2, 2, 3, 3, 2),       
    'major_sus_4': (5, 2, 5),    

}
INTERVALS = {
    "unison": 0,
    "flat_2nd": 1,
    "major_2nd": 2,
    "minor_3rd": 3,
    "major_3rd": 4,
    "perfect_4th": 5,
    "tritone": 6,
    "perfect_5th": 7,
    "minor_6th": 8,
    "major_6th": 9,
    "flat_7th": 10,
    "major_7th": 11,
    "octave": 12,
}
SONGS = {
    "howls_moving_castle": [ # [offset, chord, beats]
        (-INTERVALS["perfect_5th"],"minor_7th",3),
        (-INTERVALS["perfect_4th"],"major_♭7th",3),
        (0,"minor",3),
        (0,"minor_7th",3),
        (-INTERVALS["major_3rd"],"major_7th",3),
        (-INTERVALS["major_2nd"],"major_add2",3),
        (INTERVALS["minor_3rd"],"major",3), 
        (INTERVALS["minor_3rd"],"major_7th",3),
        (-INTERVALS["minor_3rd"],"diminished_7th",3),
        (INTERVALS["major_2nd"],"major_♭7th",3),
        (-INTERVALS["perfect_4th"],"minor_add4",3),
        (-INTERVALS["perfect_5th"],"major_6th",3),
        (-INTERVALS["major_6th"],"major_7th",3),
        (-INTERVALS["flat_7th"],"minor_7th",3),
        (-INTERVALS["perfect_4th"],"major",6),
    ],
    "fly_me_to_the_moon": [ # [offset, chord, beats]
        (0,"minor",4),
        (-INTERVALS["perfect_5th"],"minor_7th",4),
        (-INTERVALS["major_2nd"],"major",2),
        (-INTERVALS["major_2nd"],"major_♭7th",2),
        (-INTERVALS["major_6th"],"major_7th",2),
        (-INTERVALS["major_6th"],"major_♭7th",2),
        (-INTERVALS["major_3rd"],"major",2),
        (-INTERVALS["major_3rd"],"major_7th",2),
        (-INTERVALS["perfect_5th"],"minor_7th",2),
        (-INTERVALS["flat_7th"],"diminished_7th",2),
        (-INTERVALS["perfect_4th"],"major_♭7th",4),
        (0,"minor",2),
        (0,"major_♭7th",2),
        (-INTERVALS["perfect_5th"],"minor",2),
        (-INTERVALS["perfect_5th"],"minor_7th",2),
        (-INTERVALS["major_2nd"],"major",2),
        (-INTERVALS["major_2nd"],"major_♭7th",2),
        (-INTERVALS["major_6th"],"major_7th",4),
        (0,"major_♭7th",4),
        (-INTERVALS["perfect_5th"],"minor_7th",4),
        (-INTERVALS["major_2nd"],"major_sus_4",2),
        (-INTERVALS["major_2nd"],"major",2),
        (-INTERVALS["major_6th"],"major_7th",4),
        (-INTERVALS["perfect_4th"],"major",2),
        (-INTERVALS["perfect_4th"],"major_♭7th",2),
        
    ],
    "simple_twist_of_fate": [ # [offset, chord]
        (0-5,"major",4),
        (0-5,"major_7th",4),
        (0-5,"major_♭7th",4),
        (-5-INTERVALS["perfect_5th"],"major",4),
        (-5-INTERVALS["perfect_5th"],"minor",4),
        (0-5,"major",4), 
        (-5-INTERVALS["perfect_4th"],"major_sus_4",4),
        (0-5,"major",4),
    ],
    "pop 4 chords minor": [
        (0,"minor",4),
        (-INTERVALS["major_3rd"],"major",4),
        (INTERVALS["minor_3rd"],"major",4),
        (-INTERVALS["major_2nd"],"major",4),
    ],
    "pop 4 chords major": [
        (0,"major",4),
        (-INTERVALS["perfect_4th"],"major",4),
        (-INTERVALS["minor_3rd"],"minor",4),
        (-INTERVALS["perfect_5th"],"major",4),
    ],
}
SONGS["all_chords"] = [(0,x,3) for x in CHORDS]
MIDI_NOTE_NAMES = ["C","C#/D♭","D","D#/E♭","E","F","F#/G♭","G","G#/A♭","A","A#/B♭","B"]

pygame.midi.init()
player = pygame.midi.Output(0)
instrument = 1
player.set_instrument(instrument)
STARTING_NOTE = 55
while(True):
    for song_name in SONGS:
        song = SONGS[song_name]
        print("\n"+song_name)
        Dispatch("SAPI.SpVoice").Speak(song_name.replace("_"," "))
        for _ in range(2):
            last = None
            for chord in song:
                # instrument += 1
                player.set_instrument(instrument)
                offset = chord[0]
                root = STARTING_NOTE+offset
                scale = CHORDS[chord[1]]
                beats = chord[2]
                print(MIDI_NOTE_NAMES[root%12], chord[1])
                notes = [root+sum(scale[:i]) for i in range(len(scale)+1)]
                notes += [root+12+sum(scale[:i+1]) for i in range(len(scale))]
                player.note_on(notes[0]-12, 127)
                if not last: last = 6
                visited = []
                for _ in range(beats*4):
                    weights = [0 if i == last else 0 if i in visited else int(10**(2/abs((last-i)))) for i,_ in enumerate(notes)]
                    weights = [w-min(weights) for w in weights]
                    if set(weights) == {0}:
                        visited = visited[-1:]
                        weights = [0 if i == last else 0 if i in visited else int(10**(2/abs((last-i)))) for i,_ in enumerate(notes)]
                        weights = [w-min(weights) for w in weights]
                    print("arpeggio:",notes,"probability:", weights)
                    note = random.choices(notes, weights=weights)[0]
                    last = notes.index(note)
                    visited.append(last)
                    player.note_on(note, 127)
                    time.sleep(SIXTEENTH_NOTE)
                for note in notes:
                    player.note_off(note, 127)
                player.note_off(notes[0]-12, 127)
        time.sleep(SECONDS_PER_BEAT*3)


        
