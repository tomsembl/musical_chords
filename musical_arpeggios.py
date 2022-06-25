import pygame.midi, time

BPM = 160
seconds_per_beat = 60.0 / BPM
sixteenth_note = seconds_per_beat / 4

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
    "howls_moving_castle": [ # [offset, chord]
        (-INTERVALS["perfect_5th"],"minor_7th"),
        (-INTERVALS["perfect_4th"],"major_♭7th"),
        (0,"minor"),
        (0,"minor_7th"),
        (-INTERVALS["major_3rd"],"major_7th"),
        (-INTERVALS["major_2nd"],"major_add2"),
        (INTERVALS["minor_3rd"],"major"), 
        (INTERVALS["minor_3rd"],"major_7th"),
        (-INTERVALS["minor_3rd"],"diminished_7th"),
        (INTERVALS["major_2nd"],"major_♭7th"),
        (-INTERVALS["perfect_4th"],"minor_add4"),
        (-INTERVALS["perfect_5th"],"major_6th"),
        (-INTERVALS["major_6th"],"major_7th"),
        (-INTERVALS["flat_7th"],"minor_7th"),
        (-INTERVALS["perfect_4th"],"major"), 
        (-INTERVALS["perfect_4th"],"major"),
    ],
    "simple_twist_of_fate": [ # [offset, chord]
        (0,"major"),
        (0,"major_7th"),
        (0,"major_♭7th"),
        (-INTERVALS["perfect_5th"],"major"),
        (-INTERVALS["perfect_5th"],"minor"),
        (0,"major"), 
        (-INTERVALS["perfect_4th"],"major_sus_4"),
        (0,"major"),
    ],
    "pop 4 chords minor": [
        (0,"minor"),
        (-INTERVALS["major_3rd"],"major"),
        (INTERVALS["minor_3rd"],"major"),
        (-INTERVALS["major_2nd"],"major"),
    ],
    "pop 4 chords major": [
        (0,"major"),
        (-INTERVALS["perfect_4th"],"major"),
        (-INTERVALS["minor_3rd"],"minor"),
        (-INTERVALS["perfect_5th"],"major"),
    ],
}

MIDI_NOTE_NAMES = ["C","C#/D♭","D","D#/E♭","E","F","F#/G♭","G","G#/A♭","A","A#/B♭","B"]

pygame.midi.init()
player = pygame.midi.Output(0)
instrument = 0
player.set_instrument(instrument)
STARTING_NOTE = 56
while(True):
    for song_name in SONGS:
        song = SONGS[song_name]
        print("\n"+song_name)
        for _ in range(2):
            for chord in song:
                instrument += 1
                player.set_instrument(instrument)
                print(instrument,MIDI_NOTE_NAMES[chord[0]%12], chord[1])
                offset = chord[0]
                root = STARTING_NOTE+offset
                scale = CHORDS[chord[1]]
                notes = [root+sum(scale[:i]) for i in range(len(scale)+1)]
                notes += [root+12+sum(scale[:i+1]) for i in range(len(scale))]
                player.note_on(notes[0]-12, 127)
                for note in (notes+notes[::-1][1:])[:12]:
                    player.note_on(note, 127)
                    time.sleep(sixteenth_note)
                for note in notes:
                    player.note_off(note, 127)
                player.note_off(notes[0]-12, 127)


    print("\nall chords:")
    for chord_name in CHORDS:
        chord = CHORDS[chord_name]
        print(chord_name, chord)
        notes = [STARTING_NOTE+sum(chord[:i]) for i in range(len(chord)+1)]
        notes += [STARTING_NOTE+12+sum(chord[:i+1]) for i in range(len(chord))]
        player.note_on(notes[0]-24, 127)
        for note in notes+notes[::-1][1:]:
            player.note_on(note, 127)
            time.sleep(sixteenth_note)
        time.sleep(sixteenth_note*1)
        for note in notes:
            player.note_off(note, 127)


        
