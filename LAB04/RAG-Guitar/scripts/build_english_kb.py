"""
build_english_kb.py - Generate comprehensive, normalized English Guitar Knowledge Base
Combines in-depth technical guitar engineering/theory knowledge with chord database.
"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "guitar_knowledge_base.txt")
CHORD_DB_DIR = r"d:\Protae\LearningZone\3yTrem1\AdvanceML\LAB\LAB03\RAG-Project\data\guitar-chords-db-json-master"

# 1. Technical Knowledge Base (English)
QA_TOPICS = [
    # Category: Acoustic Guitars & Selection Guide
    ("Acoustic Guitars & Selection Guide", [
        ("What are the primary differences between acoustic and electric guitars?",
         "Acoustic guitars produce sound acoustically through a hollow soundbox and soundboard that amplifies string vibrations naturally without external amplification. They offer warm, natural, dynamic acoustic resonance ideal for folk, fingerstyle, pop, and unplugged performances.\nIn contrast, electric guitars feature solid or semi-hollow wood bodies and rely on electromagnetic pickups to convert string vibrations into electrical signals routed through an amplifier and effects processors. Electric guitars offer immense tonal versatility, sustained distortion, and easier playability due to thinner neck profiles and lighter string tension."),

        ("What body shape should a beginner choose for an acoustic guitar?",
         "For general versatility and strumming, a Dreadnought (41-inch) is the industry standard offering robust bass response and high acoustic volume. However, players with smaller physical frames or those focusing on fingerstyle often prefer an OM (Orchestra Model) or 000 Concert size (39-40 inches), which offers a balanced midrange and more comfortable lap ergonomics.\nFor travel or smaller hands, 3/4-scale guitars and parlor body shapes provide shorter scale lengths and closer fret spacing, significantly reducing initial finger fatigue."),

        ("How does a classical guitar differ from a steel-string acoustic guitar?",
         "Classical guitars use nylon strings, which produce a softer, mellow, and round tone with substantially less finger tension for beginners. They feature wide, flat fingerboards (usually 52mm nut width) without fretboard radius or fret markers, and are traditionally played fingerstyle for classical, flamenco, and bossa nova.\nSteel-string acoustics use metal alloy strings (phosphor bronze or 80/20 bronze) producing a bright, percussive, and ringing sound with narrower, radiused necks (typically 43mm nut width) designed for chord strumming and modern flatpicking."),

        ("What is the difference between a Dreadnought, Concert (OM), and Parlor guitar?",
         "1. Dreadnought: Large body, deep waist, high acoustic volume, booming bass response, optimized for heavy flatpicking and rhythmic strumming.\n2. Concert / OM (Orchestra Model): Narrower waist, shallower body depth, balanced frequency response across bass, mids, and treble, highly responsive to delicate fingerpicking dynamics.\n3. Parlor: Compact, vintage body shape with neck meeting the body at the 12th fret, focused mid-range punch, intimate projection, and great portability."),

        ("What is the difference between a 12-fret and a 14-fret acoustic guitar?",
         "A 12-fret acoustic guitar has its neck joined to the body at the 12th fret, placing the bridge closer to the center of the lower bout (the sweet spot of the soundboard), yielding a warmer, rounder tone with greater bass resonance.\nA 14-fret guitar joins at the 14th fret, shifting the bridge closer to the soundhole, which provides improved upper-fret accessibility and a tighter, brighter attack."),

        ("What is a cutaway on an acoustic guitar and does it affect tone?",
         "A cutaway is an indentation in the upper bout of the guitar body designed to allow the player's fretting hand easier access to the higher frets above the 12th/14th fret.\nWhile removing a small section of body volume theoretically slightly reduces air resonance, modern acoustic designs make the acoustic difference virtually imperceptible to the human ear in live and recorded contexts."),

        ("What is a 12-string guitar and how is it tuned?",
         "A 12-string guitar features six pairs (courses) of strings that produce a rich, natural chorus and shimmering jangle. The lower four string pairs (E, A, D, G) are tuned in octaves (one standard gauge string and one lighter octave string), while the top two pairs (B and high E) are tuned in unison to the same pitch: (eE aA dD gG BB EE)."),

        ("What is a carbon fiber acoustic guitar and what are its advantages?",
         "Carbon fiber guitars are manufactured using woven carbon composite materials rather than organic tonewoods. They are virtually impervious to temperature extremes, humidity fluctuations, cracking, and warping, making them the ultimate rugged instrument for touring, outdoor playing, and harsh climates while delivering consistent, bright acoustic projection."),
    ]),

    # Category: Electric Guitars & Pickup Configuration
    ("Electric Guitars & Pickup Configuration", [
        ("What are the tonal characteristics of a Fender Stratocaster?",
         "The Fender Stratocaster features a contoured double-cutaway solid alder or ash body with three single-coil pickups and a 5-way selector switch. It is famous for its bright, articulate, 'bell-like' clean chime, glassy highs, and signature 'quack' or scooped out-of-phase tones in positions 2 and 4 (bridge+middle and neck+middle).\nIt is the quintessential instrument for Blues, Funk, Classic Rock, Pop, and Neo-soul, played by legends like Jimi Hendrix, Stevie Ray Vaughan, and John Mayer."),

        ("What are the characteristics of a Gibson Les Paul?",
         "The Gibson Les Paul features a thick, solid mahogany body typically topped with a carved maple cap, a set mahogany neck, and dual Humbucking pickups with a 3-way toggle switch and independent volume/tone controls.\nIt delivers thick, warm, saturated tone with heavy low-end punch, harmonic richness, and exceptional sustain. It excels in Hard Rock, Heavy Metal, Blues-Rock, and Jazz, as popularized by Slash, Jimmy Page, and Gary Moore."),

        ("How does a Fender Telecaster differ from a Stratocaster?",
         "The Telecaster is a single-cutaway guitar with two single-coil pickups, a fixed 'ashtray' bridge with strings running through the body, and a master volume and tone circuit. The bridge pickup is mounted directly on a metal baseplate, producing the legendary high-output, cutting 'Tele twang' with aggressive bite and punch.\nWhile the Stratocaster offers smoother contours and vibrato bridge versatility, the Telecaster is renowned for simplicity, rock-solid tuning stability, and raw tonal presence across Country, Indie, and Rock."),

        ("What is the difference between Single-Coil and Humbucker pickups?",
         "Single-coil pickups use a single wire coil wrapped around magnetic pole pieces, producing bright, crisp, articulate, and transparent highs, but they are susceptible to electromagnetic 60-cycle hum and noise under high gain.\nHumbuckers use two coils wired in reverse polarity and series with opposite magnetic orientation, canceling out 60-cycle hum ('bucking the hum'). They produce a thicker, darker, higher-output signal with compressed mids that handle heavy overdrive and distortion cleanly."),

        ("What is a P-90 pickup and where does it sit tonally?",
         "A P-90 is a vintage single-coil pickup design with a wider, shorter bobbin and dual bar magnets underneath. Tonally, it bridges the gap between traditional single-coils and humbuckers: it possesses the clarity, attack, and top-end chime of a single-coil combined with the fat, gritty midrange growl and high output of a humbucker, making it iconic for Punk, Garage Rock, and Blues."),

        ("What are Active pickups and how do they differ from Passive pickups?",
         "Passive pickups generate electrical current purely through electromagnetic induction from string vibrations without external power, offering organic dynamics and natural touch sensitivity.\nActive pickups (e.g., EMG, Fishman Fluence) utilize low-impedance coils paired with an integrated active preamp powered by a 9V onboard battery. They provide ultra-high output, dead-silent noise performance, extended frequency response, and uniform clarity even under extreme high-gain distortion."),

        ("What is Coil-Splitting and Coil-Tapping?",
         "Coil-splitting refers to shutting off one coil of a 4-conductor humbucker via a push-pull pot or mini-switch, effectively converting it into a true single-coil pickup for brighter, thinner tones.\nCoil-tapping applies to high-output single coils or specialty humbuckers where a wire taps into the coil winding halfway through to reduce output and simulate vintage lower-wind pickup warmth."),

        ("What is a Semi-Hollow body guitar (e.g., Gibson ES-335)?",
         "A semi-hollow guitar features a hollow body interior with F-holes but includes a solid center block of maple or spruce running down the middle from neck to bridge. The center block eliminates high-gain feedback and increases sustain like a solid-body, while the hollow outer wings add acoustic warmth, airiness, and harmonic resonance suited for Jazz, Blues, and Indie Rock."),

        ("What is a Floyd Rose locking tremolo system?",
         "A Floyd Rose is a double-locking floating vibrato bridge system that locks the guitar strings at both the headstock nut and the bridge saddles. This dual-clamping mechanism allows radical dive-bombs and pitch bends while maintaining 100% tuning stability under aggressive playing."),
    ]),

    # Category: Tonewoods & Construction
    ("Tonewoods & Construction", [
        ("What is the acoustic difference between Solid Wood and Laminated Wood?",
         "Solid tonewood consists of single, uninterrupted planks of wood sawn directly from timber logs. Solid tops vibrate freely with superior acoustic projection, harmonic overtone complexity, and dynamic sensitivity, and they 'open up' (sound richer and warmer over time as wood resins crystallize).\nLaminate wood is constructed by gluing several thin veneers together under high pressure. While laminates are highly resistant to humidity changes, cracking, and cost significantly less, they possess lower vibrational efficiency and do not age tonally."),

        ("What are the tonal characteristics of Sitka Spruce vs Western Red Cedar?",
         "Sitka Spruce is the most popular acoustic soundboard wood, offering high stiffness-to-weight ratio, crisp dynamic headroom, punchy projection, and bell-like clarity suitable for aggressive strumming and flatpicking.\nWestern Red Cedar is softer and less dense than spruce, providing instant acoustic response, warm overtone saturation, darker harmonic bloom, and rich midrange at lower volume thresholds, making it the favorite for fingerstyle and classical playing."),

        ("How do Mahogany and Indian Rosewood compare as acoustic back and sides?",
         "Mahogany back and sides produce a focused, dry, woody, and direct tone with pronounced midrange punch, fast note decay, and minimal overtone clutter, making it exceptional for recording and cutting through a mix.\nIndian Rosewood delivers a deep, resonant low-end bass rumble, sparkling bell-like highs, and a scooped midrange with lush, reverberant harmonic overtones and long sustain."),

        ("What are the properties of Maple as a neck and fingerboard tonewood?",
         "Hard rock maple is dense, heavy, and structurally rigid, providing outstanding neck stability against string tension. Tonally, maple yields a fast transient attack, bright top-end snap, tight bass, and distinct note separation, widely used on Fender guitars for both necks and glossy or satin fretboards."),

        ("How does Rosewood compare to Ebony for guitar fretboards?",
         "Rosewood is naturally oily and open-grained with a medium density, offering a warm, velvety tactile feel and smoothing out harsh treble frequencies.\nEbony is extremely dense, heavy, tight-grained, and naturally slick, producing crisp percussive attack, snappy articulation, rapid sustain, and a luxurious dark aesthetic."),

        ("What is the difference between a Bolt-On, Set-Neck, and Neck-Through construction?",
         "1. Bolt-On (e.g., Fender Stratocaster): Neck is bolted to body pocket with 4 screws; produces snappy attack, high treble definition, and allows easy neck replacement/repair.\n2. Set-Neck (e.g., Gibson Les Paul): Neck is glued into body mortise with wood tenon; enhances midrange warmth, low-end coupling, and acoustic sustain.\n3. Neck-Through (e.g., Jackson, ESP): Central neck wood extends continuously through entire body length with side wings glued on; provides maximum sustain, seamless upper-fret heel access, and structural rigidity."),
    ]),

    # Category: Guitar Maintenance, Action & Setup
    ("Guitar Maintenance, Action & Setup", [
        ("What is guitar action and what is the standard recommended string height?",
         "Guitar action is the clearance distance between the top of the metal frets and the bottom of the guitar strings measured at the 12th fret.\nStandard recommended action heights:\n• Electric Guitar: 1.5mm - 2.0mm on low E (6th string), 1.0mm - 1.5mm on high E (1st string).\n• Steel-string Acoustic: 2.0mm - 2.5mm on low E, 1.5mm - 2.0mm on high E.\n• Classical Guitar: 3.5mm - 4.0mm on low E, 2.8mm - 3.2mm on high E.\nLower action facilitates faster playing and easier chord fretting, while higher action allows harder picking without fret buzzing."),

        ("What is a Truss Rod and how do you adjust neck relief?",
         "A truss rod is an adjustable steel rod installed inside the guitar neck beneath the fretboard to counteract string tension and regulate neck curvature (relief).\n• To fix Back-Bow (neck bending backward causing fret buzz at frets 1-5): Turn the allen wrench COUNTER-CLOCKWISE (loosen) to add forward bow/relief.\n• To fix excessive Up-Bow (neck bending forward causing high action at frets 7-12): Turn the allen wrench CLOCKWISE (tighten) in 1/4-turn increments to flatten the neck.\nAlways allow the wood 15-30 minutes to settle after adjustment."),

        ("How do you check guitar intonation and how is it adjusted?",
         "Intonation ensures every note remains in tune all the way up the fretboard.\nTo check: Tune the open string perfectly with an electronic tuner, then play the fretted note at the 12th fret.\n• If the 12th fretted note is SHARP compared to the open pitch: The string length is too short — move the bridge saddle BACKWARD (away from the neck/lengthen string).\n• If the 12th fretted note is FLAT compared to the open pitch: The string length is too long — move the bridge saddle FORWARD (toward the neck/shorten string)."),

        ("Why do guitar frets buzz and how do you troubleshoot fret buzz?",
         "Fret buzz occurs when a vibrating string rattles against a fretwire. Key causes and solutions:\n1. Open string buzz: Nut slots cut too deep (shim or replace nut).\n2. Buzz on frets 1 to 5: Insufficient neck relief/back-bow (loosen truss rod counter-clockwise).\n3. Buzz on frets 12 and above: Bridge saddles or acoustic saddle set too low (raise bridge saddles).\n4. Buzz on a single isolated fret: Uneven or popped high fret (requires fret leveling, crowning, and polishing)."),

        ("How should an acoustic guitar be protected against humidity and temperature?",
         "Acoustic guitars should ideally be stored in a relative humidity (RH) range of 45% to 55% and temperature of 20°C - 25°C (68°F - 77°F).\n• Low Humidity (<35%): Causes soundboard sinking, sharp protruding fret ends, neck warping, and wood cracks (use soundhole humidifiers like Boveda or D'Addario Humidipak).\n• High Humidity (>65%): Causes wood swelling, high action, dull acoustic volume, and glue joint softening (use silica gel desiccant packs in hardcase)."),

        ("How often should guitar strings be changed and how do you clean the fretboard?",
         "Uncoated strings should be changed every 20-40 playing hours or every 3-6 weeks as sweat and oil cause oxidation, dull tone, and intonation drift. Coated strings (e.g., Elixir Nanoweb) last 3-6 months.\nWhen changing strings: Clean unfinished rosewood/ebony fretboards using Dunlop 65 or 100% pure Lemon Oil / mineral oil with a micro-fiber cloth to condition wood and dissolve dirt (never apply lemon oil to finished maple fretboards)."),
    ]),

    # Category: Amplifiers & Effects Pedals
    ("Amplifiers & Effects Pedals", [
        ("What is the difference between Tube, Solid-State, and Digital Modeling amplifiers?",
         "1. Tube (Valve) Amps: Use vacuum tubes for preamp and power amp stages; produce warm, dynamic, touch-sensitive compression, natural harmonic overdrive, and organic punch.\n2. Solid-State Amps: Use transistors and analog circuits; produce pristine clean headroom, reliable operation, lightweight builds, and lower maintenance costs.\n3. Digital Modeling / Profiling (e.g., Neural DSP Quad Cortex, Line 6 Helix, Kemper): Use DSP algorithms to mathematically replicate hundreds of vintage tube amps, speaker cabinets (IRs), and studio effects with 100% consistency and direct recording outputs."),

        ("What is the signal chain order for guitar effects pedals?",
         "The standard recommended pedalboard signal chain is:\n1. Dynamics & Pitch: Tuner → Wah → Pitch Shifter / Whammy → Compressor\n2. Gain / Drive: Boost → Overdrive → Distortion → Fuzz\n3. Equalization: EQ pedal (can also sit in FX loop)\n4. Modulation: Chorus → Flanger → Phaser → Tremolo (often placed in Amp FX Loop)\n5. Time-Based & Ambient: Delay → Reverb (placed at end of chain or in Amp FX Loop)\n6. Volume / Utility: Volume pedal, Looper, Noise Gate."),

        ("What is the difference between Overdrive, Distortion, and Fuzz?",
         "• Overdrive: Soft-clipping circuit simulating a tube amp driven just past clean breakup; dynamic, responsive to picking attack, preserves original guitar note clarity.\n• Distortion: Hard-clipping circuit providing uniform saturation, sustain, aggressive harmonics, and compression regardless of picking dynamics (e.g., BOSS DS-1, ProCo Rat).\n• Fuzz: Extreme transistor clipping (germanium/silicon) that squares off waveforms completely, yielding thick, buzzing, synth-like, chaotic vintage sustain (e.g., Electro-Harmonix Big Muff, Fuzz Face)."),

        ("What is an Effects Loop (FX Loop) and why should you use it?",
         "An Effects Loop places effects pedals between the amplifier's Preamp section (where preamp gain/overdrive is created) and Power Amp section.\nPlacing time-based pedals (Delay, Reverb, Chorus) in the FX Loop prevents delay repeats and reverb tails from being distorted and turned to muddy noise by high-gain preamp distortion, ensuring pristine, crystal-clear echoes."),

        ("What is an Impulse Response (IR) in guitar modeling?",
         "An Impulse Response (IR) is an advanced digital acoustic measurement capturing the exact acoustic resonance, frequency response, and phase characteristics of a specific guitar speaker cabinet, speaker cone, microphone model, mic placement angle, and studio room reflection."),
    ]),

    # Category: Music Theory, Scales & Solos
    ("Music Theory, Scales & Solos", [
        ("What is the Minor Pentatonic Scale and why is it essential for guitar solos?",
         "The Minor Pentatonic Scale is a 5-note scale derived from the Natural Minor scale by removing the 2nd and 6th scale degrees: Formula = 1 - b3 - 4 - 5 - b7.\nIn the key of A minor, the notes are: A - C - D - E - G.\nBecause it eliminates half-step dissonances, it is the foundational scale for Rock, Blues, Pop, and Metal improvisation, fitting effortlessly over minor and dominant 7th chord progressions."),

        ("What is the Blues Scale and what is the 'Blue Note'?",
         "The Blues Scale is created by adding a flattened 5th (b5) — known as the 'Blue Note' — to the standard Minor Pentatonic scale: Formula = 1 - b3 - 4 - b5 - 5 - b7.\nIn the key of A Blues, the notes are: A - C - D - D# (Eb) - E - G.\nThe chromatic tension of the b5 gives the scale its signature soulful, gritty, bluesy cry when bent or resolved to the 4th or 5th degree."),

        ("What are the 7 Major Scale Modes?",
         "The 7 modes are diatonic scales derived by starting on each consecutive degree of the Major scale (Ionian):\n1. Ionian (1-2-3-4-5-6-7) : Major / Happy\n2. Dorian (1-2-b3-4-5-6-b7) : Minor with bright raised 6th / Funky, Jazzy Blues\n3. Phrygian (1-b2-b3-4-5-b6-b7) : Minor with dark b2 / Flamenco, Metal\n4. Lydian (1-2-3-#4-5-6-7) : Major with ethereal #4 / Dreamy, Sci-Fi\n5. Mixolydian (1-2-3-4-5-6-b7) : Major with b7 / Southern Rock, Blues\n6. Aeolian (1-2-b3-4-5-b6-b7) : Natural Minor / Melodic, Somber\n7. Locrian (1-b2-b3-4-b5-b6-b7) : Diminished / Unresolved, Tense."),

        ("What is the CAGED System on the guitar fretboard?",
         "The CAGED system is a fretboard visualization framework linking 5 open chord shapes (C, A, G, E, D) across all 12 positions of the guitar neck.\nEvery chord, arpeggio, and pentatonic/major scale box connects sequentially in the cycle C-A-G-E-D-C along the fretboard, allowing guitarists to play any chord or solo in any key anywhere on the neck."),

        ("What is the Circle of Fifths and how is it used?",
         "The Circle of Fifths is a geometric clock-like representation of all 12 chromatic pitches showing their key signatures and harmonic relationships. Moving clockwise adds one sharp (#) via ascending 5ths (C, G, D, A, E, B, F#), while moving counter-clockwise adds one flat (b) via ascending 4ths (C, F, Bb, Eb, Ab, Db, Gb).\nIt is used to determine key signatures, transpose chords, find relative minor keys, and construct harmonic chord progressions (e.g., ii-V-I)."),
    ]),

    # Category: Playing Techniques & Exercises
    ("Playing Techniques & Exercises", [
        ("What is Alternate Picking and how do you practice it?",
         "Alternate picking is the fundamental picking technique of strictly alternating downward and upward pick strokes (Down-Up-Down-Up) in continuous subdivision.\nPractice by setting a metronome at 60 BPM playing 16th notes on single strings and chromatic 1-2-3-4 permutations, ensuring pick depth is minimal, wrist remains relaxed, and pick angle is slanted slightly (15-20 degrees)."),

        ("What is the difference between Legato and Staccato playing?",
         "Legato is a smooth, fluid phrasing technique where notes are connected seamlessly using Hammer-ons, Pull-offs, and Slides with minimal right-hand picking, producing a vocal-like fluidity (famous in Allan Holdsworth and Joe Satriani solos).\nStaccato is playing notes sharply detached, shortened, and muted immediately after attack, giving crisp percussive rhythm."),

        ("What is Sweep Picking and how is it executed?",
         "Sweep picking is an advanced technique used to play fast arpeggios across adjacent strings with a single continuous downward or upward 'raking' stroke of the pick.\nSynchronization requires the fretting hand to fret only one note at a time and immediately release finger pressure (rolling the finger) to mute previous strings so notes ring individually as an arpeggio rather than a strummed chord."),

        ("What is a Pinch Harmonic (Squeal) and how do you produce it?",
         "A pinch harmonic is executed by striking the string with the guitar pick and immediately brushing the side of the picking-hand thumb against the vibrating string node in a single motion, canceling the fundamental frequency and triggering a high-pitched artificial harmonic overtone, which is then emphasized with wide vibrato."),

        ("What is Travis Picking in acoustic fingerstyle?",
         "Travis picking is a fingerpicking technique named after Merle Travis where the thumb maintains a steady, syncopated alternating bass line on the lower three strings (beats 1, 2, 3, 4) while the index and middle fingers independently pluck syncopated melody and chord harmony on the treble strings."),
    ]),
]

# Standard Chord Suffixes to extract from Chord DB
PRIMARY_CHORD_SUFFIXES = [
    ("major.json", "Major", "Major triad"),
    ("minor.json", "Minor", "Minor triad"),
    ("7.json", "7", "Dominant 7th chord"),
    ("maj7.json", "maj7", "Major 7th chord"),
    ("m7.json", "m7", "Minor 7th chord"),
    ("sus2.json", "sus2", "Suspended 2nd chord"),
    ("sus4.json", "sus4", "Suspended 4th chord"),
    ("dim.json", "dim", "Diminished triad"),
    ("dim7.json", "dim7", "Diminished 7th chord"),
    ("aug.json", "aug", "Augmented triad"),
    ("add9.json", "add9", "Add 9 chord"),
    ("5.json", "5", "Power chord (Root + 5th)"),
    ("6.json", "6", "Major 6th chord"),
    ("m6.json", "m6", "Minor 6th chord"),
    ("9.json", "9", "Dominant 9th chord"),
    ("m9.json", "m9", "Minor 9th chord"),
    ("maj9.json", "maj9", "Major 9th chord"),
    ("m7b5.json", "m7b5", "Half-diminished 7th chord"),
    ("7sus4.json", "7sus4", "7th Suspended 4th chord"),
]

STRING_NAMES = ["6 (Low E)", "5 (A)", "4 (D)", "3 (G)", "2 (B)", "1 (High E)"]

def parse_fret_char(char):
    if char in ('x', 'X'):
        return "Mute / Do not play (x)"
    if char == '0':
        return "Open string (0)"
    if char.isdigit():
        return f"Fret {char}"
    # hex-like or alphabetic frets (a=10, b=11, c=12, d=13, e=14, f=15)
    char_map = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'k': 19, 'm': 21}
    val = char_map.get(char.lower(), char)
    return f"Fret {val}"

def extract_chords_from_db():
    extracted = []
    if not os.path.exists(CHORD_DB_DIR):
        print(f"Warning: {CHORD_DB_DIR} does not exist.")
        return extracted

    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    for key in keys:
        key_dir = os.path.join(CHORD_DB_DIR, key)
        if not os.path.exists(key_dir):
            continue

        for filename, suffix_name, chord_type_desc in PRIMARY_CHORD_SUFFIXES:
            file_path = os.path.join(key_dir, filename)
            if not os.path.exists(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                positions = data.get("positions", [])
                if not positions:
                    continue

                full_chord_name = f"{key} {suffix_name}" if suffix_name != "Major" and suffix_name != "Minor" else (f"{key} Major" if suffix_name == "Major" else f"{key} Minor ({key}m)")
                symbol = f"{key}{suffix_name}" if suffix_name not in ("Major", "Minor") else (key if suffix_name == "Major" else f"{key}m")

                # Take up to 2 primary voicings (e.g. open/low position vs barre)
                for pos_idx, pos in enumerate(positions[:2], start=1):
                    frets = pos.get("frets", "")
                    if len(frets) != 6:
                        continue

                    voicing_title = f"{full_chord_name} ({symbol})" if pos_idx == 1 else f"{full_chord_name} ({symbol}) - Voicing Position {pos_idx}"
                    fret_pattern = "-".join(list(frets))

                    ans_lines = [
                        f"The {full_chord_name} ({chord_type_desc}) is fretted and voiced across the 6 strings (from Low E to High E) with fret pattern [{fret_pattern}]:"
                    ]
                    for s_idx, char in enumerate(frets):
                        ans_lines.append(f"- String {STRING_NAMES[s_idx]}: {parse_fret_char(char)}")

                    barre = pos.get("barres")
                    if barre:
                        ans_lines.append(f"- Barre Note: Barre across fret {barre} using the index finger.")

                    q_text = f"How do you play the {symbol} ({full_chord_name}) chord on guitar?" if pos_idx == 1 else f"How do you play the alternative voicing of {symbol} ({full_chord_name}) on guitar?"
                    a_text = "\n".join(ans_lines)

                    extracted.append((
                        "Guitar Chord Fingerings & Voicings",
                        q_text,
                        a_text
                    ))
            except Exception as e:
                pass

    return extracted

def main():
    lines = [
        "# Comprehensive English Guitar Knowledge Base & Chord Reference (LAB04: RAG-Guitar)",
        "# Purpose: Optimized for English dense semantic retrieval (BAAI/bge-small-en-v1.5) and BM25",
        "# Structure: [Category: Category Name] + Q: Question + A: Answer",
        "# ====================================================================================\n"
    ]

    total_count = 0

    # 1. Add In-depth Technical Guitar Knowledge
    for category, pairs in QA_TOPICS:
        for q, a in pairs:
            lines.append(f"[Category: {category}]")
            lines.append(f"Q: {q.strip()}")
            lines.append(f"A: {a.strip()}\n")
            total_count += 1

    # 2. Add Normalized Guitar Chords from DB
    chord_records = extract_chords_from_db()
    for cat, q, a in chord_records:
        lines.append(f"[Category: {cat}]")
        lines.append(f"Q: {q.strip()}")
        lines.append(f"A: {a.strip()}\n")
        total_count += 1

    content = "\n".join(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Generated normalized English Guitar Knowledge Base with {total_count} records at {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
