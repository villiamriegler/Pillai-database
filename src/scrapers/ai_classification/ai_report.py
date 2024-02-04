
#pip install nltk spacy ReportLab tensorflow terminators
#python -m spacy download en_core_web_sm
import json
import tensorflow as tf
import numpy as np
import random
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
import spacy
import glob

MAX_POSITIVES = 2000     # The maximum number of positive texts

# Model to detect spaces
nlp = spacy.load("en_core_web_sm")

# Function to split text into sentences using Spacy
def get_sentences(text):
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

# Map scores to correct color
def get_color(score):
    # Boundary colors
    red = (0xde, 0x5e, 0x47)    # 0.0
    white = (255, 255, 255)     # 0.5
    green = (0x45, 0xb0, 0x73)  # 1.0
    
    if score <= 0.5:
        # Lower bound
        percentage = score * 2  # Transforms score to percentage
        target_r = int(red[0] + (white[0] - red[0]) * percentage)
        target_g = int(red[1] + (white[1] - red[1]) * percentage)
        target_b = int(red[2] + (white[2] - red[2]) * percentage)
    
    else:
        # Upper bound
        percentage = (score - 0.5) * 2  # Transforms score to percentage
        target_r = int(white[0] + (green[0] - white[0]) * percentage)
        target_g = int(white[1] + (green[1] - white[1]) * percentage)
        target_b = int(white[2] + (green[2] - white[2]) * percentage)
    
    # Return resulting color
    return f'#{target_r:02x}{target_g:02x}{target_b:02x}'

def write_output(sentances, scores, filename="results.html"):
    # Read the HTML template
    with open('template.html', 'r') as file:
        html_template = file.read()
        
    # Initialize empty body content
    content = ""

    # Generate content
    for i, (sentences, combined_scores) in enumerate(zip(sentances, scores)):
        # New section with title
        content += f'<div class="paper"><div class="title">Text {i+1}</div>'
        
        # Create and format all sentances
        for sentence, score in zip(sentences, combined_scores):
            color = get_color(score)
            content += f'<span class="sentence" style="background-color:{color};">{sentence}</span>'
        content += '</div>'
    
    # Replace the placeholder in the template with the actual content
    html_content = html_template.replace('<!--CONTENT_PLACEHOLDER-->', content)
    
    # Write the modified HTML to a new file
    with open(filename, 'w') as file:
        file.write(html_content)
    print(f"HTML file created: {filename}")



# Function to load and extract texts from JSON
# Function to load and extract texts from multiple JSON files
def get_texts(directory, max_entries=MAX_POSITIVES):
    related_texts = []      # Positives
    unrelated_texts = []    # Negatives

    # List all JSON files in the specified directory
    json_files = glob.glob(f'{directory}/*.json')
    
    count = 0

    # Load all JSON data
    for json_file in json_files:
        count += 1
        if count == MAX_POSITIVES:
            break
        with open(json_file, 'r') as file:
            data = json.load(file)

        # Check both 'bipacksedel' and 'fass_text' keys in each file
        for key in ['bipacksedel', 'fass_text']:
            if key in data:
                if "pregnancy" in data[key]:
                    related_texts.append(data[key]["pregnancy"])
                # Use other fields as unrelated data
                for field in ["appearance", "composition", "product-form", "storage", "prod-license", "tradename", 
                              "caution", "caution-and-warnings", "user-information", "driving", "side-effects", 
                              "missed", "overdosage", "usage-and-administration",]:
                    if field in data[key]:
                        unrelated_texts.append(data[key][field])

            # Check max entries
            if len(related_texts) >= max_entries and len(unrelated_texts) >= max_entries:
                break

    # Limit to max entries
    related_texts = related_texts[:max_entries]
    unrelated_texts = unrelated_texts[:max_entries*4]

    # Combine and label texts [1] for positive and [0] for negative
    texts = related_texts + unrelated_texts
    labels = [1] * len(related_texts) + [0] * len(unrelated_texts)

    # Shuffle combined data since order should not matter
    combined = list(zip(texts, labels))
    random.shuffle(combined)
    texts, labels = zip(*combined)

    return texts, labels

# Preprocess the data
def preprocess_texts(texts):
    tokenizer = Tokenizer(num_words=100000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)

    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=MAX_POSITIVES, padding='post')

    return padded_sequences, tokenizer

# Building the model
def build_model():
    model = Sequential([
        Embedding(100000, 16, input_length=MAX_POSITIVES),
        GlobalAveragePooling1D(),
        Dense(24, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Training the model
def train_model(model, data, labels):
    labels = np.array(labels)
    model.fit(data, labels, epochs=10, verbose=2)

# Scoring any input texts
def score_texts(model, tokenizer, texts):
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=MAX_POSITIVES, padding='post')
    return model.predict(padded)


def main():
    # Load and preprocess texts
    texts, labels = get_texts('../data/products')
    train_data, tokenizer = preprocess_texts(texts)

    # Build and train the model
    model = build_model()
    train_model(model, train_data, labels)

    alvedon_full = """"
    Alvedon
500 mg munsönderfallande tabletter
paracetamol
Läs noga igenom denna bipacksedel innan du börjar använda detta läkemedel. Den innehåller information som är viktig för dig.
Använd alltid detta läkemedel exakt enligt beskrivning i denna bipacksedel eller enligt anvisningar från din läkare, apotekspersonal eller sjuksköterska.
Spara denna information, du kan behöva läsa den igen.
Vänd dig till apotekspersonalen om du behöver mer information eller råd.
Om du får biverkningar, tala med läkare, apotekspersonal eller sjuksköterska. Detta gäller även eventuella biverkningar som inte nämns i denna information. Se avsnitt 4.
Du måste tala med läkare om symtomen försämras eller inte förbättras inom 3 dagar vid feber och 5 dagar vid smärta.

I denna bipacksedel finner du information om:
1. Vad Alvedon är och vad det används för
2. Vad du behöver veta innan du använder Alvedon
3. Hur du använder Alvedon
4. Eventuella biverkningar
5. Hur Alvedon ska förvaras
6. Förpackningens innehåll och övriga upplysningar
1. Vad Alvedon är och vad det används för
 
Alvedon innehåller paracetamol som är smärtlindrande och febernedsättande.
Alvedon används för behandling av tillfälliga feber- och smärttillstånd av lindrig art, t ex feber vid förkylning, huvudvärk, tandvärk, menstruationssmärtor, muskel- och ledvärk.
Alvedon kan användas även om du har känslig mage eller magsår eller om du har ökad benägenhet för blödningar.

2. Vad du behöver veta innan du använder Alvedon
Använd inte Alvedon
om du är allergisk mot paracetamol eller något annat innehållsämne i detta läkemedel (anges i avsnitt 6).
om du har kraftigt nedsatt leverfunktion.

Varningar och försiktighet
Alvedon innehåller paracetamol. Om du använder andra smärtstillande läkemedel som innehåller paracetamol ska du inte använda Alvedon utan att först tala med läkare eller apotekspersonal.
Ta aldrig mer Alvedon än vad som står under doseringsanvisningen.
Högre doser än de rekommenderade ger inte bättre smärtlindring utan medför istället risk för mycket allvarlig leverskada. Symtomen på leverskada kommer normalt först efter ett par dagar. Därför är det viktigt att du kontaktar läkare omedelbart om du har tagit för stor dos, även om du mår bra.
Använd inte Alvedon utan läkares ordination om du har alkoholproblem eller leverskada och använd heller inte Alvedon tillsammans med alkohol. Berusnings­effekten av alkohol ökar inte genom tillägg av Alvedon.

Tala med läkare innan du använder Alvedon om du:
har nedsatt lever- eller njurfunktion.
har astma och samtidigt är känslig för acetylsalicylsyra.
har brist på ett enzym som heter glukos-6-fosfatdehydrogenas.
är undernärd eller underviktig på grund av otillräckligt kostintag eller felaktig kosthållning eller om du har en allvarlig infektion såsom blodförgiftning. Detta p.g.a. ökad risk för:
leverskada
metabolisk acidos. Tecken på metabolisk acidos inkluderar: djup, snabb, ansträngd andning; illamående, kräkningar; aptitlöshet. Kontakta genast läkare om du får en kombination av dessa symtom.

Andra läkemedel och Alvedon
Tala om för läkare eller apotekspersonal om du använder eller nyligen har använt eller kan tänkas använda andra läkemedel. Alvedon kan påverka eller påverkas av vissa läkemedel, (traditionella) växtbaserade läkemedel eller naturläkemedel. Kontakta därför apotekspersonal eller läkare innan du använder Alvedon tillsammans med något av följande läkemedel.
blodförtunnande läkemedel (t.ex. warfarin och andra kumariner). Enstaka doser av Alvedon anses inte påverka effekten av warfarin. Ta högst 2 tabletter Alvedon (à 500 mg) per dygn under 5 dagar i följd, för vuxen. Behöver du ta mer kontakta läkare först.
probenecid (läkemedel mot gikt)
vissa läkemedel mot epilepsi:
- fenytoin
- fenobarbital
- karbamazepin
rifampicin (läkemedel mot tuberkulos)
kolestyramin (läkemedel vid höga blodfetter). Medicinerna bör tas med minst en timmes mellanrum.
kloramfenikol för injektion (läkemedel vid bakterieinfektioner). Kloramfenikol mot infektioner i ögat och Alvedon kan användas samtidigt.
johannesörtextrakt (ingår i vissa (traditionella) växtbaserade läkemedel och naturläkemedel)

Alvedon med mat, dryck och alkohol
Alvedon kan tas med eller utan mat.Använd inte Alvedon tillsammans med alkohol, se avsnittet ”Varningar och försiktighet”.

Graviditet och amning
Om du är gravid eller ammar, tror att du kan vara gravid eller planerar att skaffa barn, rådfråga läkare eller apotekspersonal innan du använder detta läkemedel.
Om så är nödvändigt kan Alvedon användas under graviditet. Du ska dock använda lägsta möjliga dos som lindrar din smärta och/eller din feber och använda den under kortast möjliga tid. Kontakta din läkare eller barnmorska om smärtan och/eller febern inte minskar eller om du behöver ta läkemedel oftare.
Paracetamol passerar över i modersmjölk, men påverkar troligen inte barn som ammas. Tala ändå med läkare vid mer än tillfällig användning av Alvedon under amning.

Körförmåga och användning av maskiner
Alvedon påverkar inte din förmåga att köra bil eller använda maskiner.
Alvedon innehåller aspartam
Alvedon innehåller aspartam som omvandlas till fenylalanin. Kan vara skadligt för personer med fenylketonuri (en medfödd ämnesomsättningssjukdom).

3. Hur du använder Alvedon
Använd alltid detta läkemedel exakt enligt beskrivning i denna bipacksedel eller enligt anvisningar från läkaren, apotekspersonal eller sjuksköterska. Rådfråga läkare, apotekspersonal eller sjuksköterska om du är osäker.
Observera! Högre doser än de rekommenderade innebär risk för mycket allvarlig leverskada.
Ta aldrig mer Alvedon än vad som står under doseringsanvisningarna. Använd alltid lägsta möjliga dos som ger dig lindring av dina symtom, under så kort behandlingstid som möjligt.
Om du har nedsatt lever- eller njurfunktion eller har Gilberts syndrom bör du rådfråga din läkare om lämplig dos, eftersom den kan behöva justeras nedåt.



Rekommenderad dos är:
Vuxna och ungdomar över 40 kg (över 12 år):
1-2 tabletter var 4-6 timme, högst 8 tabletter per dygn.
Kontakta läkare om symtomen försämras eller inte förbättras inom 3 dagar vid feber och 5 dagar vid smärta.
Användning för barn under 40 kg (under 12 år)
Alvedon 500 mg munsönderfallande tabletter ska inte användas av barn som väger mindre än 40 kg eller av barn under 12 år.

Bruksanvisning
Låt tabletten smälta på tungan och svälj därefter direkt. Det behövs inget vatten. Tabletten ska inte tuggas.
Tabletten kan även lösas upp i ca ½ glas vatten. Rör om väl.

Öppningsanvisning
Tabletten ligger i ett barnskyddande blister. Riv av en ruta från tablettkartan längs med den perforerade linjen. Dra sedan av foilen och ta ut tabletten, se bild nedan. Du ska alltså inte trycka ut tabletten genom blistret.
Öppningssinstruktion

Om du använt för stor mängd av Alvedon 
Om du fått i dig för stor mängd läkemedel eller om t.ex. ett barn fått i sig läkemedlet av misstag kontakta omedelbart läkare, sjukhus eller Giftinformationscentralen (tel. 112) för bedömning av risken samt rådgivning.
Överdosering av paracetamol kan ge allvarlig leverskada med risk för dödlig utgång. Det finns risk för leverskada även om man mår bra. 
För att förhindra leverskada är det viktigt att få medicinsk behandling så tidigt som möjligt. Ju kortare tid som går mellan överdosering och påbörjad behandling med motgift (så få timmar som möjligt), desto större chans är det att leverskada kan förebyggas.

4. Eventuella biverkningar
Liksom alla läkemedel kan Alvedon orsaka biverkningar men alla användare behöver inte få dem.

Sluta att ta Alvedon och kontakta omedelbart läkare om du upplever något av följande. Ring eventuellt 112:
Sällsynta (kan förekomma hos upp till 1 av 1 000 användare):
Angioödem, mycket allvarlig allergisk reaktion:
svullnad av ansikte, tunga eller svalg
svårigheter att svälja
nässelutslag och andningssvårigheter
Allergiska reaktioner som hudutslag och nässelfeber. Även mindre allvarliga former av hudreaktioner, utslag och klåda kan förekomma.
Leverpåverkan. Detta kan vara mycket allvarligt och kan ge symtom som trötthet, illamående, kräkningar, magbesvär och aptitlöshet.
Mycket sällsynta (kan förekomma hos upp till 1 av 10 000 användare):
Blödning från hud och slemhinnor och blåmärken, allmän slöhet, tendens till inflammation (infektioner) särskilt halsont och feber på grund av förändringar i blodet (minskat antal vita blodkroppar och blodplättar).
Allvarliga andningssvårigheter med flämtande andning.
Njurbiverkningar
Blekhet, trötthet och gulsot på grund av allvarlig blodbrist.
Mycket sällsynta fall av allvarliga hudreaktioner har rapporterats.
Anafylaxi: överkänslighetsreaktion med feber, hudutslag, svullnad och ibland blodtrycksfall.

Rapportering av biverkningar
Om du får biverkningar, tala med läkare, apotekspersonal eller sjuksköterska. Detta gäller även eventuella biverkningar som inte nämns i denna information. Du kan också rapportera biverkningar direkt till Läkemedelsverket, www.lakemedelsverket.se. Genom att rapportera biverkningar kan du bidra till att öka informationen om läkemedels säkerhet.  Postadress

5. Hur Alvedon ska förvaras
Förvaras utom syn- och räckhåll för barn och ungdomar.
Används före det utgångsdatum som står på förpackningen. Utgångsdatumet är den sista dagen i angiven månad.
Läkemedel ska inte kastas i avloppet eller bland hushållsavfall. Fråga apotekspersonalen hur man kastar läkemedel som inte längre används. Dessa åtgärder är till för att skydda miljön.

6. Förpackningens innehåll och övriga upplysningar
Innehållsdeklaration
Den aktiva substansen är paracetamol 500 mg
Övriga innehållsämnen är: Mannitol 686,1 mg, krospovidon, aspartam, magnesiumstearat, polymetakrylater, kolloidal vattenfri kiseldioxid, smakämne (svartvinbärssmak innehållande citron-, apelsin-, vanilj- och mintessenser).

Läkemedlets utseende och förpackningsstorlekar
Vita, runda tabletter utan delningsskåra, diameter 17 mm. Tabletten har smak av svartvinbär.
    """
    # Test scoring with different texts
    new_texts =  ["Sample text to score", 
                "Om du är gravid eller ammar, tror att du kan vara gravid eller planerar att skaffa barn, rådfråga läkare eller apotekspersonal innan du använder detta läkemedel.", 
                "Matematisk teori är ett ypperligt tillfälle att lära sig att analysera, resonera, argumentera, strukturera och ordna. Matematik bygger på abstraktion och den som lär sig att lätt ta till sig abstraktion besitter en enorm styrka i analytiska sammanhang.",
                "Paracetamol (systematiskt namn: N(4-hydroxifenyl)acetamid) är ett febernedsättande (antipyretikum) och smärtstillande (analgetikum) läkemedel som i Sverige bland annat säljs receptfritt under varunamnen Alvedon, Panodil med flera. Vid föreskriven användning är det ovanligt med biverkningar.",
                "Normal dos av paracetamol anses ofarligt för gravida kvinnor och har inte visats ge någon högre andel missbildningar hos fostren.[24] Paracetamol kan användas vid graviditet och amning. Visserligen går lite av ämnet ut i modersmjölken men vid normal användning är det för lite för att påverka barnet.",
                "Du som är gravid kan ha rätt till graviditetspenning. Det gäller om du har ett fysiskt ansträngande arbete, eller om det finns risker i arbetsmiljön och din arbetsgivare inte kan omplacera dig till andra arbetsuppgifter.",
                "Eva hade alltid drömt om att resa jorden runt, uppleva nya kulturer och se världens underverk med egna ögon. Efter år av sparande och planering började hon äntligen sin resa med en ryggsäck fylld av förväntningar och en lista över platser att besöka. Hon vandrade genom Europas historiska städer, förlorade sig i Asiens pulserande marknader och fann frid vid Sydamerikas avlägsna stränder. Livet var en äventyrsbok, och varje dag skrev hon ett nytt kapitel. Men allt förändrades när hon mötte Carlos i en liten kafé i Barcelona. Deras kärlek blommade snabbt, och inom några månader upptäckte Eva att hon var gravid. Plötsligt fylldes hennes värld av en annan sorts förväntan. Resan hon påbörjat ensam hade tagit en oväntad vändning, och nu förberedde hon sig för livets största äventyr: moderskapet. Graviditeten blev en resa i sig, en resa genom känslor, förväntningar och drömmar om framtiden. Tanken på att bli mamma var överväldigande, men också fylld av en kärlek hon aldrig tidigare känt. Hennes dagar av oändlig vandring hade lett henne till en ny början, och hon omfamnade denna förändring med öppet hjärta, redo för de nya äventyr som väntade henne och hennes lilla familj.",
                "Alvedon 500 mg munsönderfallande tabletter ska inte användas av barn som väger mindre än 40 kg eller av barn under 12 år.",
                "Vanligen räknas graviditetens första dag från den senaste menstruationens första dag, det vill säga innan ägget är befruktat,[1][2] vilket ger en genomsnittlig graviditetslängd på 40 veckor innan den gravida i en vaginal förlossning eller genom kejsarsnitt framföder barnet. Föds barnet tidigare än vecka 37 brukar man räkna det som för tidigt fött; sådana barn kallas prematura.[3] Att barn föds från vecka 37 och fram till vecka 42 brukar räknas som normalt. Finns mer än en äggcell tillgänglig kan alla befruktas av var sin spermie med en senare flerbarnsbörd som resultat (tvillingar, trillingar eller flera; varje ägg kan dock normalt endast befruktas av en spermie och motsatsen leder till spontanabort). Enäggstvillingar uppstår ur ett enda befruktat ägg. Genom graviditetstest med urinprov är graviditet möjlig att fastställa 10 till 12 dagar efter att menstruationen uteblivit.[5] BIM (beräknad icke mens) är den förväntad första dag för utebliven mens vid graviditet.[6] Kvinnan ändrar hormoncykel och brösten kan öka i storlek och kännas spända. En del kvinnor upplever stark trötthet, andra mer eller mindre kraftigt illamående och många kvinnor kräks på morgnarna under de första tre månaderna av graviditeten. Under dessa månader så syns inte graviditeten utanpå kvinnan eftersom embryot är så litet att livmodern fortfarande är belägen i lilla bäckenet.",
                "Artificiell intelligens (AI) eller maskinintelligens är förmågan hos datorprogram och robotar att efterlikna människors och andra djurs naturliga intelligens,[1] främst kognitiva funktioner såsom förmåga att lära sig saker av tidigare erfarenheter, förstå naturligt språk, lösa problem, planera en sekvens av handlingar och att generalisera.[2][3] Det är också namnet på det akademiska studieområde som studerar hur man skapar datorprogram med intelligent beteende. Exempel på äldre delområde och metodik är expertsystem, medan mer aktuella delområden är maskininlärning, databrytning (datamining), datorseende, stora språkmodeller och generativ AI(en). Exempel på tillämpningsområden är maskinläsning, röststyrning, maskinöversättning, chattbotar, digitala assistenter, business intelligence, ansiktsigenkänning, deepfake, självkörande bilar och autonoma vapensystem. Många AI-forskare och AI-läroböcker definierar området som 'studiet och utformningen av intelligenta agenter', där en intelligent agent är ett system som uppfattar sin omgivning och vidtar åtgärder som maximerar sina chanser att framgångsrikt uppnå sina mål. John McCarthy, som myntade begreppet 1956[4], definierar det som 'vetenskapen och tekniken att skapa intelligenta maskiner'.[5] De främsta problemen (eller målen) för AI-forskningen är bland annat: resonemang, kunskap, planering, inlärning, naturlig språkbearbetning (kommunikation), perception och förmåga att flytta och manipulera objekt.",           
                "Kan tas under graviditet. Det finns inga kända risker vid användning under graviditet. Magnesiumhydroxid går över i modersmjölk, men påverkar troligen inte barn som ammas. Rådgör dock med läkare vid mer än tillfälligt bruk av Magnesium Evolan under amning.",
                "Läkemedlet kan tas utan risk för biverkningar vid graviditet. Förtär det dock en timme innan du går och lägger dig.",
                "Vid användning av detta läkemedel är det viktigt att noggrant överväga riskerna och fördelarna, särskilt under graviditet och amningstiden. Om du är gravid, planerar att bli gravid, eller ammar, bör du rådgöra med din läkare innan du påbörjar behandlingen med detta läkemedel.",
                "Användning av läkemedelsnamn rekommenderas inte under graviditetens första trimester och bör endast användas under andra och tredje trimestern om den potentiella nyttan överväger den möjliga risken för fostret. Det finns begränsad data om användningen av läkemedelsnamn hos gravida kvinnor. Djurstudier har visat en viss risk, men den fullständiga risken för människor är inte känd. Om du upptäcker att du är gravid under behandlingen, kontakta omedelbart din läkare för rådgivning.",
                "Läkemedelsnamn utsöndras i modersmjölk i små mängder. En risk för det ammande barnet kan inte uteslutas. Beslutet att fortsätta/amma eller att fortsätta/avstå från behandlingen med läkemedelsnamn bör göras med beaktande av nyttan av amning för barnet och nyttan av behandlingen för modern. Rådgör med din läkare om de bästa alternativen för dig och ditt barn.",
                "Det finns inga eller begränsade data med avseende på effekten av läkemedelsnamn på mänsklig fertilitet. Djurstudier har visat ingen eller endast minimala effekter på fertiliteten. Om du planerar att bli gravid, diskutera dina behandlingsalternativ med din läkare.",
                alvedon_full,
    ]
    sentances = []  # Split into scentances
    scores = []  # Scores for scentances

    for text in new_texts:
        sentences = get_sentences(text)  # Split each text into sentences
        
        # Score the whole paragraph
        paragraph_score = score_texts(model, tokenizer, [text]).flatten()[0]
        
        # Score each sentence
        sentence_scores = score_texts(model, tokenizer, sentences).flatten()
        
        # Combine paragraph score with individual sentence scores
        combined_scores = [(0.3 * paragraph_score + 0.7 * s) for s in sentence_scores]
        
        sentances.append(sentences)  # Add list of sentences for this text block
        scores.append(combined_scores)  # Add corresponding combined scores

    # Generate a single HTML file for all text blocks with combined scores
    write_output(sentances, scores, filename="result.html")
    

if __name__ == "__main__":
    main()
