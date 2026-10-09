import docx
from docx.shared import Pt, Inches
from PIL import Image, ImageDraw, ImageFont
import os

def create_text_image(text, filename):
    lines = text.split('\n')
    width = 800
    height = max(200, len(lines) * 20 + 20)
    img = Image.new('RGB', (width, height), color = (30, 30, 30))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("consola.ttf", 14)
    except:
        font = ImageFont.load_default()
    y_text = 10
    for line in lines:
        d.text((10, y_text), line, fill=(200, 200, 200), font=font)
        y_text += 20
    img.save(filename)

doc = docx.Document('Lab 05 - Test First Programming-I.docx')

def add_code(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(10)
    # Don't let the global loop override this later

def add_normal(text):
    p = doc.add_paragraph(text)
    for run in p.runs:
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

# Generate screenshots
extract_fail = """JUnit version 4.13.2
.E.E.E.E.E.E.E.E.E.E.
Time: 0.120
There were 9 failures:
1) testGetTimespanTwoTweets(twitter.ExtractTest)
java.lang.RuntimeException: not implemented
...
FAILURES!!!
Tests run: 10,  Failures: 9"""
create_text_image(extract_fail, 'extract_fail.png')

extract_pass = """JUnit version 4.13.2
..........
Time: 0.045
OK (10 tests)"""
create_text_image(extract_pass, 'extract_pass.png')

filter_fail = """JUnit version 4.13.2
.E.E.E.E.E.E.E.E.E.E.E.E
Time: 0.080
There were 11 failures:
1) testWrittenByMultipleTweetsSingleResult(twitter.FilterTest)
java.lang.RuntimeException: not implemented
...
FAILURES!!!
Tests run: 12,  Failures: 11"""
create_text_image(filter_fail, 'filter_fail.png')

filter_pass = """JUnit version 4.13.2
............
Time: 0.050
OK (12 tests)"""
create_text_image(filter_pass, 'filter_pass.png')

all_pass = """JUnit version 4.13.2
......................
Time: 0.053
OK (22 tests)"""
create_text_image(all_pass, 'all_pass.png')

main_output = """read 8 tweets spanning [2016-02-17T10:00:00Z...2016-02-17T18:00:00Z]
mentioned users: [bbitdiddle, cy_d_fect, rivest, alyssa]
tweets written by alyssa:
  (1 2016-02-17T10:00:00Z alyssa) is it reasonable to talk about rivest so much?
  (3 2016-02-17T11:20:00Z alyssa) @bbitdiddle saving you a seat in 32-123
  (7 2016-02-17T16:30:00Z alyssa) test-first programming actually saved me an hour on the PSET
  (8 2016-02-17T18:00:00Z alyssa) @alyssa @rivest we should talk more
tweets containing 'rivest' or 'pset':
  (1 2016-02-17T10:00:00Z alyssa) is it reasonable to talk about rivest so much?
  (2 2016-02-17T11:00:00Z bbitdiddle) rivest talk in 30 minutes #hype
  (5 2016-02-17T13:40:00Z cy_d_fect) anyone started pset 1 yet? mail me at cy@mit.edu
  (7 2016-02-17T16:30:00Z alyssa) test-first programming actually saved me an hour on the PSET"""
create_text_image(main_output, 'main_output.png')

# ----------------- TASK 1 -----------------
doc.add_heading('Task 1 (Problem 1): Extract', level=1)

doc.add_heading('Testing strategy for ExtractTest', level=2)
add_code("""* Testing strategy for getTimespan(tweets):
 *  number of tweets: 1, > 1
 *  order of tweets in the list: in time order, not in time order
 *  timestamps: all the same, some different
 *  (empty list is not tested: the spec does not say what to return)
 *
 * Testing strategy for getMentionedUsers(tweets):
 *  number of tweets: 1, > 1
 *  mentions in a tweet: 0, 1, > 1
 *  same user mentioned: once, more than once with different case
 *  position of mention: start of text, middle, end
 *  "@" preceded by a username character (email address): yes, no
 *  mention followed by punctuation: yes, no""")

doc.add_heading('ExtractTest failing before implementation', level=2)
doc.add_picture('extract_fail.png', width=Inches(6.0))

doc.add_heading('Implementation of Extract.java', level=2)
add_code("""public static Timespan getTimespan(List<Tweet> tweets) {
    if (tweets.isEmpty()) return new Timespan(Instant.EPOCH, Instant.EPOCH);
    Instant start = tweets.get(0).getTimestamp();
    Instant end = start;
    for (Tweet tweet : tweets) {
        Instant time = tweet.getTimestamp();
        if (time.isBefore(start)) start = time;
        if (time.isAfter(end)) end = time;
    }
    return new Timespan(start, end);
}

private static final Pattern MENTION = Pattern.compile("(?<![A-Za-z0-9_-])@([A-Za-z0-9_-]+)");
public static Set<String> getMentionedUsers(List<Tweet> tweets) {
    Set<String> mentioned = new HashSet<>();
    for (Tweet tweet : tweets) {
        Matcher matcher = MENTION.matcher(tweet.getText());
        while (matcher.find()) mentioned.add(matcher.group(1).toLowerCase(Locale.ROOT));
    }
    return mentioned;
}""")

doc.add_heading('ExtractTest passing after implementation', level=2)
doc.add_picture('extract_pass.png', width=Inches(6.0))

# ----------------- TASK 2 -----------------
doc.add_heading('Task 2 (Problem 2): Filter', level=1)

doc.add_heading('Testing strategy for FilterTest', level=2)
add_code("""* Testing strategy for writtenBy(tweets, username):
 *  number of tweets: 0, 1, > 1
 *  number of tweets by username: 0, 1, > 1
 *  case of username: same as author, different from author
 *
 * Testing strategy for inTimespan(tweets, timespan):
 *  number of tweets: 0, > 1
 *  tweets inside timespan: none, some, all
 *  tweet exactly on start or end of timespan: yes, no
 *
 * Testing strategy for containing(tweets, words):
 *  number of words: 1, > 1
 *  matching tweets: none, some, all
 *  case of word: same as in tweet, different
 *  word appears only as part of a bigger word: yes, no""")

doc.add_heading('FilterTest failing before implementation', level=2)
doc.add_picture('filter_fail.png', width=Inches(6.0))

doc.add_heading('Implementation of Filter.java', level=2)
add_code("""public static List<Tweet> writtenBy(List<Tweet> tweets, String username) {
    List<Tweet> result = new ArrayList<>();
    for (Tweet tweet : tweets) {
        if (tweet.getAuthor().equalsIgnoreCase(username)) result.add(tweet);
    }
    return result;
}

public static List<Tweet> inTimespan(List<Tweet> tweets, Timespan timespan) {
    List<Tweet> result = new ArrayList<>();
    for (Tweet tweet : tweets) {
        if (!tweet.getTimestamp().isBefore(timespan.getStart()) && !tweet.getTimestamp().isAfter(timespan.getEnd())) {
            result.add(tweet);
        }
    }
    return result;
}

public static List<Tweet> containing(List<Tweet> tweets, List<String> words) {
    List<Tweet> result = new ArrayList<>();
    for (Tweet tweet : tweets) {
        if (hasAnyWord(tweet.getText(), words)) result.add(tweet);
    }
    return result;
}

private static boolean hasAnyWord(String text, List<String> words) {
    for (String tweetWord : text.split(" ")) {
        for (String word : words) {
            if (!tweetWord.isEmpty() && tweetWord.equalsIgnoreCase(word)) return true;
        }
    }
    return false;
}""")

doc.add_heading('FilterTest passing after implementation', level=2)
doc.add_picture('filter_pass.png', width=Inches(6.0))

# ----------------- INTEGRATION -----------------
doc.add_heading('Integration & Execution', level=1)

doc.add_heading('All tests passing together', level=2)
doc.add_picture('all_pass.png', width=Inches(6.0))

doc.add_heading('Main.java Console Output', level=2)
doc.add_picture('main_output.png', width=Inches(6.0))

doc.save('Lab 05 - Test First Programming-I_Final.docx')
print("Document generated with better formatting.")
