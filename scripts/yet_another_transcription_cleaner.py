#!/usr/bin/python3

import sys
import os

if len(sys.argv) < 4:
    print( "Usage: python3 %s INFILE PROMPT_OUTFILE UTTERANCE_LIST_OUTFILE OPTIONS" % sys.argv[0])
    sys.exit(9)

infile = sys.argv[1]
promptsoutfile = sys.argv[2]
uttlistoutfile = sys.argv[3]

overwrite=False

if len(sys.argv) > 4:
    for argm in sys.argv[4:]:
        if argm == '-o' or argm == '--overwrite':
            overwrite=True
    
if not os.path.exists(infile):
    print( "Error: Input file %s does not exist!" % sys.argv[1])
    sys.exit(9)
    

if os.path.exists(promptsoutfile) and not overwrite:
    print( "Error: Outputfile %s exists!" % promptsoutfile)
    print( "Run with option -o to overwrite")
    sys.exit(9)

if os.path.exists(uttlistoutfile) and not overwrite:
    print( "Error: Outputfile %s exists!" % uttlistoutfile)
    print( "Run with option -o to overwrite")
    sys.exit(9)


    
import re
import unicodedata

alphabet=u'[A-ZÅÖÄa-zåöäÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜáíóúñÑß-]+'
alphabet_and_hyphen=u'[A-ZÅÖÄa-zåöäÇüéâäàåçêëèïîìÄÅÉæÆôöòûùÿÖÜáíóúñÑß\'-]+'

stress=u'[?!¿¡]'


meta_marking_mappings = {
    '[/bad_mic_position]' : '[speech_quality_issue]',
    '[/beep]': '[misc_noise]',
    '[/chair_squeak]': '[misc_noise]',
    '[/disk_noise]': '[misc_noise]',
    '[/door_open]': '[misc_noise]',
    '[/door_slam]': '[misc_noise]' ,
    '[/laughing]' : '[laughter]',
    '[/laughter]' : '[laughter]' ,
    '[/loud]' : '[speech_quality_issue]',
    '[/microphone_mvt]' : '[speech_quality_issue]',
    '[/poor_mic_position]': '[speech_quality_issue]',
    '[/singing]': '[speech_quality_issue]',
    '[/slow]' : '[speech_quality_issue]',
    '[/soft]' : '[speech_quality_issue]',
    '[/squeak]': '[misc_noise]',
    '[<beep]': '[misc_noise]',
    '[<chair_squeak]': '[misc_noise]',
    '[<click]': '[misc_noise]',
    '[<cross_talk]': '[unintelligible]',
    '[<phone_ring]': '[misc_noise]',
    '[<tap]': '[misc_noise]',
    '[<thump]': '[misc_noise]',
    '[bad_mic_position/]' : '[speech_quality_issue]',
    '[beep/]': '[misc_noise]',
    '[beep>]' : '[misc_noise]',
    '[bn]' : '[background_noise]',
    '[bs]' : '[background_speech]',
    '[chair_squeak/]': '[misc_noise]',
    '[chair_squeak>]': '[misc_noise]',
    '[chair_squeak]': '[misc_noise]',
    '[click]' : '[misc_noise]',
    '[cough]': '[throat_clear]',
    '[cross_talk>]': '[unintelligible]' ,
    '[cross_talk]': '[unintelligible]',
    '[disk_noise/]': '[misc_noise]',
    '[disk_noise]': '[misc_noise]',
    '[door_open/]': '[misc_noise]',
    '[door_open>]' : '[misc_noise]',
    '[door_slam/]' : '[misc_noise]',
    '[exhalation]' : '[loud_breath]',
    '[footsteps]' : '[misc_noise]',
    '[grunt]' : '[throat_clear]',
    '[inhalation]' : '[loud_breath]',
    '[laughing/]' : '[laughter]',
    '[laughing>]': '[laughter]',
    '[laughter/]': '[laughter]',
    '[lip-smack]' : '[lip_smack]',
    '[lip_smaack]': '[lip_smack]',
    '[ln]' : '[bad_recording]',
    '[loud/]' : '[speech_quality_issue]',
    '[loud_beath]' : '[loud_breath]',
    '[loud_noise]' : '[misc_noise]',
    '[microphone_mvt/]' : '[speech_quality_issue]',
    '[microphone_mvt>]' : '[speech_quality_issue]',
    '[microphone_mvt]' : '[speech_quality_issue]',
    '[movement]' : '[speech_quality_issue]',
    '[phone-ring]' : '[misc_noise]',
    '[poor_mic_position/]': '[speech_quality_issue]',
    '[sigh]' : '[loud_breath]',
    '[singing/]' : '[speech_quality_issue]',
    '[slow/]' : '[speech_quality_issue]',
    '[soft/]' : '[speech_quality_issue]',
    '[squeak/]': '[misc_noise]',
    '[squeak]': '[misc_noise]',
    '[tap>]': '[misc_noise]',
    '[tap]': '[misc_noise]',
    '[thump>]': '[misc_noise]',
    '[thump]': '[misc_noise]',
    '[unitelligible]': '[unintelligible]',

    # SPEECON:

    # The [fil] marker is used to denote filled pauses.
    # Examples of typical filled pauses are uh, um, er, ah and mm.
    '[fil]' : '[filled_pause]',
        
    # The [spk] marker denotes all kind of noises and sounds made by the speaker
    # that are not part of prompted text. Examples of speaker noise are lip smack,
    # cough, loud breath, loud sigh and throat click.
    '[spk]' : '[speaker_noise]',

    # The [int] marker denotes noises of intermittent nature. These noises typically
    # occur only once (like a door slam), or have pauses between them (like phone ringing),
    # or change their colour over time (like music).}
    '[int]' : '[misc_noise]',
    
    # The [sta] marker is used for stationary noise. This category contains background
    # noise that is not intermittent and has a more or less stable amplitude spectrum
    # over some time. Examples: voice babble, public place background noise, wind, rain.
    '[sta]' : '[background_noise]'
}
    

meta_marking_brackets = { '[speech_quality_issue]' : { 'tag' : '',
                                                    'connected' : 'accept' },
                          '[loud_breath]' : { 'tag' : '[NSN:loud_breath]',
                                              'connected' : 'accept' },
                          '[speaker_noise]' : { 'tag' : '[NSN:speaker_noise]',
                                                'connected' : 'accept' },
                          '[mike_overload>]': { 'tag' : '',
                                                'connected' : 'accept' },
                          '[bad_recording]': { 'tag' : '',
                                               'connected' : 'accept' },
                          '[mouse_click]': { 'tag' : '[NSN:mouse_click]',
                                             'connected' : 'accept' },
                          '[<mike_overload]': { 'tag' : '',
                                                'connected' : 'accept' },
                          '[<misc_noise]': { 'tag' : '',
                                             'connected' : 'accept' },
                          '[<loud_breath]': { 'tag' : '[NSN:loud_breath]',
                                              'connected' : 'accept' },
                          '[lip_smack]': { 'tag' : '[NSN:lip_smack]',
                                           'connected' : 'accept' },
                          '[other_mouth_sound]': { 'tag' : '[NSN:lip_smack]',
                                                   'connected' : 'accept' },
                          '[loud_breath>]': { 'tag' : '[NSN:loud_breath]',
                                              'connected' : 'accept' },
                          '[mike_overload/]': { 'tag' : '',
                                                'connected' : 'accept' },
                          '[/mike_overload]': { 'tag' : '',
                                                'connected' : 'accept' },
                          '[mike_overload]': { 'tag' : '',
                                               'connected' : 'accept' },
                          '[phone_ring]': { 'tag' : '[NSN:phone_ring]',
                                            'connected' : 'accept' },
                          '[tongue_click]': { 'tag' : '[NSN:tongue_click]',
                                              'connected' : 'accept' },
                          '[unintelligible]': { 'tag' : '[SPN:unintelligible]',
                                                'connected' : 'reject' },
                          '[elongated]': { 'tag' : '[SPN:unintelligible]',
                                           'connected' : 'reject' },
                          '[throat_clear]': { 'tag' : '[NSN:throat_clear]',
                                              'connected' : 'accept' },
                          '[background_speech]': { 'tag' : '[SPN:background_speech]',
                                                   'connected' : 'accept' },
                          '[background_noise]': { 'tag' : '',
                                                  'connected' : 'accept' },
                          '[beep]' : { 'tag' : '[NSN:beep]',
                                       'connected' : 'accept' },
                          '[pause]' : { 'tag' : '[SIL]',
                                        'connected' : 'reject' },
                          '[filled_pause]' : { 'tag' : '[SPN:filled_pause]',
                                               'connected' : 'accept' },
                          '[laughter]' : { 'tag' : '[NSN:laughter]',
                                           'connected' : 'accept' },
                          '[singing]' : { 'tag' : '',
                                          'connected' : 'accept' },
                          '[sneeze]' : { 'tag' : '[NSN:sneeze]',
                                         'connected' : 'accept' },
                          '[whispered]': { 'tag' : '',
                                           'connected' : 'accept' },
                          '[yawn]': { 'tag' : '[NSN:yawn]',
                                      'connected' : 'accept' },
                          '[door_slam]': { 'tag' : '[NSN:misc_noise]',
                                           'connected' : 'accept' },
                          '[misc_noise]': { 'tag' : '[NSN:misc_noise]',
                                            'connected' : 'accept' },
                          '[movement/]': { 'tag' : '',
                                           'connected' : 'accept' },
                          '[/movement]': { 'tag' : '',
                                           'connected' : 'accept' },
                          '[door_slam>]' : { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[<door_slam]' : { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[paper_rustle]': { 'tag' : '[NSN:misc_noise]',
                                              'connected' : 'accept' },
                          '[paper_rustle/]' : { 'tag' : '',
                                                'connected' : 'accept' },
                          '[/paper_rustle]': { 'tag' : '',
                                               'connected' : 'accept' },
                          '[sniff]': { 'tag' : 'NSN:sneeze',
                                       'connected' : 'accept',},
                          '[mispronunciation]' : { 'tag' : '[SPN:mispronunciation]',
                                                   'connected' : 'reject',},
                          '[footsteps/]': { 'tag' : '[NSN:misc_noise]',
                                            'connected' : 'accept' },
                          '[/footsteps]': { 'tag' : '[NSN:misc_noise]',
                                            'connected' : 'accept' },
                          '[misc_noise/]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[/misc_noise]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[/misc_noise]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[phone_ring/]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[/phone_ring]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[knocking/]': { 'tag' : '[NSN:misc_noise]',
                                           'connected' : 'accept' },
                          '[/knocking]': { 'tag' : '[NSN:misc_noise]',
                                           'connected' : 'accept' },
                          '[uh]': { 'tag' : 'uh',
                                    'connected' : 'reject' },
                          '[um]': { 'tag' : 'um',
                                    'connected' : 'reject' },
                          '[eh]': { 'tag' : 'eh',
                                    'connected' : 'reject' },
                          '[er]': { 'tag' : 'er',
                                    'connected' : 'reject' },
                          '[ah]' : { 'tag' : 'ah',
                                     'connected' : 'reject' },
                          '[mm]' : { 'tag' : 'mm',
                                     'connected' : 'reject' },
                          '[cross_talk/]': { 'tag' : '[SPN:cross_talk]',
                                             'connected' : 'accept' },
                          '[/cross_talk]': { 'tag' : '[SPN:cross_talk]',
                                             'connected' : 'accept' },
                          '[loud-breath]': { 'tag' : '[NSN:loud_breath]',
                                             'connected' : 'accept' },
                          '[misc_noise>]': { 'tag' : '[NSN:misc_noise]',
                                             'connected' : 'accept' },
                          '[typing/]': { 'tag' : '[NSN:misc_noise]',
                                         'connected' : 'accept' },
                          '[/typing]': { 'tag' : '[NSN:misc_noise]',
                                         'connected' : 'accept' },
                          '[loud-breath]': { 'tag' : '[NSN:loud_breath]',
                                             'connected' : 'accept' },

}

meta_marking_angles = { 
    '<asp>' : '[unintelligible]',
    '<beep>' : '[beep]',
    '<blip>' : '[bad_recording]',
    '<bn>' : '[background_noise]',
    '<br>' : '[loud_breath]',
    '<br.'  : '[loud_breath]',
    '<<bs>' : '[background_speech]',
    '<bs>' : '[background_speech]',
    '<bs: can you des*>' : '[background_speech]',
    '<bs: dave>' : '[background_speech]',
    '<bs. four years old wow <bn>' : '[background_speech]',
    '<bs: no no>' : '[background_speech]',
    '<cough>' : '[throat_clear]',
    '<ct>' : '[throat_clear]',
    '<fp>' : '[filled_pause]',
    '<lau>' : '[laughter]',
    '<laugh>' : '[laughter]',
    '<ln>' : '[bad_recording]',
    '<long>' : '[elongated]',
    '<long<bn>' : '[elongated]',
    '<ls>' : '[lip_smack]',
    '<n>' : '[unintelligible]',
    '<nitl>' : '[unintelligible]', # Not-in-target-language
    '<ns>' : '[unintelligible]', # non-speech ?
    '<pau>' : '[pause]',
    '<pf>' : '[unintelligible]',
    '<pron>' : '[unintelligible]', # Odd pronunciation
    '<sing>' : '[singing]',
    '<sing<bn>' : '[singing]',
    '<sneeze>' : '[sneeze]',
    '<sniff>' : '[sneeze]',
    '<sp>' : '[unintelligible]', # Unknown spelling
    '<tc>' : '[tongue_click]',
    '<uu>' : '[unintelligible]',
    '<whisper>' : '[whispered]',
    '<yawn>' : '[yawn]',
    '<ns.' : '[unintelligible]',
    '<bs.' : '[background_speech]'}


wsj_hyp = ['.PERIOD',
           '\\"DOUBLE\\-QUOTE',
           '\\"DOUBLE-QUOTE',
           '\-HYPHEN',
           '\,COMMA',
           '\\"END\\-QUOTE',
           '\\"END\\-QUOTE',
           '\%PERCENT',
           '\\"QUOTE',
           '\\"QUOTES',
           '\\"UNQUOTE',
           '.POINT',
           '\~PARAGRAPH',
           '\\(PARENTHESES',
           '\\)CLOSE\\-PARENTHESES',
           '\\"CLOSE\\-QUOTES',
           '\\"CLOSE\\-QUOTE',
           '\\"OPEN\\-QUOTES',
           '\\"OPEN\\-QUOTE',
           '\:COLON',
           '\!EXCLAMATION\-POINT',
           '\-\-DASH',
           '\)PAREN',
           '\?QUESTION-MARK',
           '\?QUESTION\\-MARK',
           '\-EM\-DASH',
           '\~NEW\-GRAPH',
           '\~NEW\-PARAGRAPH',
           '\&AMPERSAND',
           '\~TITLE',
           '\~NEW\-STORY',
           '\~TITLE',
           '\~NEW\-TOPIC',
           '\~GRAPH',
           '\~NEW\-TITLE',
           '\~NEXT\-GRAPH',
           '\~NEW\-TITLE',
           '\~NEW\-WORD',
           '\(LEFT-PAREN',
           '\)RIGHT-PAREN',
           '\(LEFT\-PAREN',
           '\)RIGHT\-PAREN',
           '\(PAREN',
           '\(IN\-PAREN',
           '\!EXCLAMATION-POINT',
           '\\"CLOSE\-DOUBLE\-QUOTES',
           '\\"CONTINUE\-QUOTE',
           '\\"END-OF-QUOTE',
           '\\"END-QUOTE',
           '\\"END\-OF\-QUOTATION\-MARK',
           '\\"END\-OF\-QUOTE',
           '\\"END\-QUOTATION\-MARK',
           '\\"END\-QUOTATION\-MARKS',
           '\\"IN\-QUOTES',
           '\\"I\-QUOTE',
           '\\"QUOTATION\-MARK',
           '\\"UNQUOTES',
           '\$DOLLAR\-SIGN',
           '\&AMPERSANDS',
           '\(BEGIN\-PARENS',
           '\(BRACE',
           '\(BRACKET',
           '\(IN\-PARENTHESES',
           '\(IN\-PARENTHESIS',
           '\(LEFT\-PARENTHESES',
           '\(OPEN\-PAREN',
           '\(OPEN\-PARETHESES',
           '\(PARENS',
           '\(PARENTHESIS',
           '\(PARENTHETICALLY',
           '\)CLOSE\-BRACE',
           '\)CLOSE\-PAREN',
           '\)CLOSE\-PARENTHESIS',
           '\)CLOSE_PAREN',
           '\)END\-OF\-BRACKET',
           '\)END\-OF\-PAREN',
           '\)END\-PAREN',
           '\)END\-PARENS',
           '\)END\-PARENTHESES',
           '\)END\-THE\-PAREN',
           '\)PARENS',
           '\)PARENTHESES',
           '\)RIGHT\-PARENTHESES',
           '\)UN\-PARENTHESES',
           '\-DASH',
           '\/SLASH',
           '\;SEMI-COLON',
           '\;SEMI\-COLON',
           '\`SINGLE\-QUOTE',
           '\\\'SINGLE\-QUOTE',
           '\{BRACKETS',
           '\{LEFT-BRACE',
           '\{LEFT\-BRACE',
           '\}CLOSE\-BRACKETS',
           '\}RIGHT-BRACE',
           '\}RIGHT\-BRACE',
           '\~*NEW*\-PARAGRAPH',
           '\~ALL\-CAPS',
           '\~A\-PARAGRAPH',
           '\~CAPITAL',
           '\~END\-OF\-STORY',
           '\~END\-OF\-TITLE',
           '\~END\-OF\-TOPIC',
           '\~FOOTNOTE',
           '\~IN\-ITALICS',
           '\~NEW\-SENTENCE',
           '\~SPELLED',
           '\~STORY\-NUMBER\-FOUR',
           '\~STORY\-NUMBER\-TWO',
           '\~THAT\'S\-SPELLED',
           '...ELLIPSIS',
           '.DECIMAL',
           '.DOT',
           '.PERCENT',
           '.PERI',
           '.S.',
           '\\\'END\\-QUOTE',
           '\\\'END\\-INNER\\-QUOTE',
           '\\\'CLOSE\\-SINGLE\\-QUOTES',
           '\\\'INNER\\-QUOTE',
           '\\\'CLOSE\\-SINGLE\\-QUOTE',
           '\\\'SINGLE\\-CLOSE\\-QUOTE',
           
]

def clean_row(r):
    utt, r = re.split('\s+', r, 1)
    
    r = r.strip()
    r = r.replace('\t', ' ')
    r = r.replace('“', '"')
    r = r.replace('”', '"')
    r = r.replace('„', '"')
    r = r.replace('’', '\'')
    r = r.replace('‘', '\'')
    # Annoyng little detail on the CSLU kids transcriptions:
    if '<bs:' in r:
        re.sub('<bs:[^>]>', '<bs>', r)

    # Spraakbanken special:
    r = r.replace(',\\Komma', ' komma')
    r = r.replace('.\\Punkt', ' punkt')
    if len(r) > 1 and r[0] in ['\'', '"'] and r[-1] == r[0]:
        r = r[1:-1]
    return utt, r.split()
                 
not_handled_well = []

def clean_word(w):
    w = w.strip()
    
    # If word is empty (length 0), return none:
    if len(w) == 0:
        return None

    # Some single letter special codes:
    
    # A tilde '~' marks that recording has been cut off from start or beginnng 
    if w == '~' or  w == '~~' or w == '…':
        return None

    # A lonely dot "." marks a pause in WSJ
    if w == '.' or w == '..' or w == '...' or w == '\\.':
        return '[pause]'

    # A lonely comma ',' does not mean anything?
    if w == ',':
        return None
    
    # Normalise unicode:
    w = unicodedata.normalize('NFC', w)

    # Does the word start with quotation? Not anymore!
    if w[0] == '"':
        w = w[1:]
        if len(w) == 0:
            return None
        # Does it for some reason still start with quotation?
        if w[0] == '"':
            w = w[1:]
            if len(w) == 0:
                return None

    # ... or inverted exclamation or question mark ¿¡
    if w[0] in '¿¡':
        w = w[1:]
        if len(w) == 0:
            return None

    # Does it have a ')' with no '(' in it?
    if ')' in w and '(' not in w:
        w = w.replace(')', '')
    # Does it start with a '(' with no ')' in it?
    if w[0] == '(' and ')' not in w:
        w = w[1:]
        
    # Does it end in comma ',', question, exclamation and quotation mark, or combination:
    # Not anymore!
    w = re.sub('[,!?";\.]+$', '', w)
    if len(w) == 0:
        return None

    # Does it for whatever reason end in a backslash '\'?
    if w[-1] == '\\':
        w = w[:-1]
    
    # The hash '#' in the middle of a string means a replacement in speecon:
    # Use the second half of the string:
    if '#' in w[1:-1]:
        w = w.split('#')[1]
    # '_' in the beginning of speecon word label means a non-standard pronunciation.
    # These are very well transcribed in Finnish so let's remove the underscore and keep!
    if w[0] == '_':
        w=w[1:]

    # in WSJ, a dash '-' at the beginning or end of a word means it is cut off:
    if w[0] == '-' or w[-1] == '-':
        return '[SPN:mispronunciation]'
        
    # Match only alpabet from start to end:
    m = re.match(alphabet+'$', w)
    if m:
        return w
    # Match only numerals from start to end:
    if re.match(r'[0-9]+', w):
        return w

    # An exclamation mark '!' at the beginning or in the middle of the word
    # means an uncommon stress. We don't want that for our mispronunciation detector:
    if '!' in w[:-1]:
        return '[SPN:mispronunciation]'

    # A colon ":" marks a lengthened phone in WSJ -- Too much work to go through these,
    # so ditch for now:
    if ':' in w:
        return '[SPN:mispronunciation]'

    # in CLSU, a star in the beginning or end of word means the word has been cut off.
    # in WSJ(?) stars in both ends mean a strange pronunciation variant
    #if w[0] == '*' or w[-1] == '*':
    if '*' in w:
        return '[SPN:mispronunciation]'
    # The same (maybe?) in common voice Italian but with triple-dot symbol?
    if '…' in w:
        return '[SPN:mispronunciation]'
    
    # Else, parts of words in parenthesis mean they are no pronounced:
    if '(' in w and ')' in w:
        return '[mispronunciation]'

    if '<' in w or '>' in w:
        # Check for CLSU labelling, eg. <laugh>
        for q in meta_marking_angles.keys():
            if q in w:
                # map to bracketed quality specifications
                b = meta_marking_brackets[meta_marking_angles[q]]
                # Do we include the attached 
                if b['connected'] == 'accept':
                    #print(w,'->',w.replace(q, ' '+b['tag']))
                    return clean_word(w.replace(q, '') + ' '+b['tag'])
                else:
                    #print(w,'=>',b['tag'])                        
                    return b['tag']
        # WSJ self corrections are in brackets;
        # Remove them and call this function again:
        if w[0] == '<' and w[-1] == '>':
            return clean_word(w[1:-1])


    # WSJ has some datasets with hyphenation spoken out loud:
    if w in wsj_hyp:
        w= re.sub('[^A-Z]+', ' ', w).strip()
        #print ('-->', w)
        return w
        
    # Normalise hyphen to '\'' 
    if '`' in w:
        w = w.replace('`', '\'')

    # Some dashes are escaped, some are not :(
    if "'" in w[1:] or '.' in w[1:]:
        w = w.replace('\\\'', '\'')
        w = w.replace('\\.', '.')
        # If only alphabet and hyphen, accept:
        m = re.match(alphabet_and_hyphen+'((\.$)|(\.\'s$))?', w)
        if m:
            return w
        #else:
        #    print ("No match in %s" % w)


    # Brackets normally mean some metadata regarding audio quality or noise:
    if '[' in w:
        for q in meta_marking_brackets.keys():
            if q in w:
                return meta_marking_brackets[q]['tag']
        for qm in meta_marking_mappings.keys():
            if qm in w:
                return meta_marking_brackets[meta_marking_mappings[qm]]['tag']


    # Does the string start with parenthesis? Not anymore!
    if w[0] == '(':
        w = w[1:]


    
    # An escaped dash?
    w = w.replace('\\', '')
    m = re.match(alphabet+'$', w)
    if m:
        return w
    
    # Else the string did not fit into any category:
    if w not in not_handled_well:
        not_handled_well.append(w)
        #print (w)
    return '[SPN:incomprehensible]'
    
promptsouthandle = open(promptsoutfile, 'w')
list_of_words = {}
list_of_utts = {}

for row in open(infile, 'r').readlines():
    outwords = []
    utt, r = clean_row(row)
    for word in r:
        cleaned_words = clean_word(word)
        if cleaned_words is not None:
            #if '\\' in cleaned_word:
            #    foo()
            for cleaned_word in cleaned_words.split():
                outwords.append(cleaned_word)
                if cleaned_word not in list_of_words.keys():
                    list_of_words[cleaned_word] = 1
                else:
                    list_of_words[cleaned_word] += 1
    if len(outwords) > 0:
        uttstring = ' '.join(outwords)
        promptsouthandle.write(utt +'\t' + uttstring +'\n')
        if uttstring not in list_of_utts.keys():
            list_of_utts[uttstring] = 1
        else:
            list_of_utts[uttstring] += 1

    else:
        promptsouthandle.write(utt +'\t' + '[SIL]\n')

promptsouthandle.close()

uttlistouthandle = open(uttlistoutfile, 'w')
for k,v in list_of_words.items():
    uttlistouthandle.write('%i\tword:\t%s\n' %(v, k))
for k,v in list_of_utts.items():
    uttlistouthandle.write('%i\tutterance:\t%s\n' % (v, k))

uttlistouthandle.close()

for w in sorted(not_handled_well):
    print('\''+w+'\'')
