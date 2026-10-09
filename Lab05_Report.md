# Lab 05: Test-First Programming: Tweet

## Task 1: Extracting data from Tweets

In this task, we implemented the `getTimespan` and `getMentionedUsers` methods in `Extract.java` and wrote JUnit test cases in `ExtractTest.java`.

### Source Code: `Extract.java`

```java
package twitter;

import java.util.List;
import java.util.Set;
import java.util.HashSet;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Locale;

public class Extract {

    public static Timespan getTimespan(List<Tweet> tweets) {
        if (tweets.isEmpty()) {
            return new Timespan(java.time.Instant.EPOCH, java.time.Instant.EPOCH);
        }
        java.time.Instant start = tweets.get(0).getTimestamp();
        java.time.Instant end = start;
        for (Tweet tweet : tweets) {
            java.time.Instant time = tweet.getTimestamp();
            if (time.isBefore(start)) {
                start = time;
            }
            if (time.isAfter(end)) {
                end = time;
            }
        }
        return new Timespan(start, end);
    }

    private static final Pattern MENTION = Pattern.compile("(?<![A-Za-z0-9_-])@([A-Za-z0-9_-]+)");

    public static Set<String> getMentionedUsers(List<Tweet> tweets) {
        Set<String> mentioned = new HashSet<>();
        for (Tweet tweet : tweets) {
            Matcher matcher = MENTION.matcher(tweet.getText());
            while (matcher.find()) {
                mentioned.add(matcher.group(1).toLowerCase(Locale.ROOT));
            }
        }
        return mentioned;
    }
}
```

### Test Case Implementation: `ExtractTest.java`

```java
package twitter;

import static org.junit.Assert.*;
import java.time.Instant;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import org.junit.Test;

public class ExtractTest {
    
    private static final Instant d1 = Instant.parse("2016-02-17T10:00:00Z");
    private static final Instant d2 = Instant.parse("2016-02-17T11:00:00Z");
    private static final Instant d3 = Instant.parse("2016-02-17T12:30:00Z");
    
    private static final Tweet tweet1 = new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", d1);
    private static final Tweet tweet2 = new Tweet(2, "bbitdiddle", "rivest talk in 30 minutes #hype", d2);
    private static final Tweet tweet3 = new Tweet(3, "alyssa", "@bbitdiddle saving you a seat, ask @Evaluator too", d3);
    private static final Tweet tweet4 = new Tweet(4, "evaluator", "thanks @BBitDiddle! mail me at eval@mit.edu", d2);
    private static final Tweet tweet5 = new Tweet(5, "cy_d_fect", "see you there @cy-d-fect_2", d1);
    
    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    
    @Test
    public void testGetTimespanOneTweet() {
        Timespan timespan = Extract.getTimespan(Arrays.asList(tweet2));
        assertEquals("expected start", d2, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());
    }

    @Test
    public void testGetTimespanTwoTweets() {
        Timespan timespan = Extract.getTimespan(Arrays.asList(tweet1, tweet2));
        assertEquals("expected start", d1, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());
    }

    @Test
    public void testGetTimespanUnorderedTweets() {
        Timespan timespan = Extract.getTimespan(Arrays.asList(tweet3, tweet1, tweet2));
        assertEquals("expected start", d1, timespan.getStart());
        assertEquals("expected end", d3, timespan.getEnd());
    }

    @Test
    public void testGetTimespanSameTimestamps() {
        Timespan timespan = Extract.getTimespan(Arrays.asList(tweet1, tweet5));
        assertEquals("expected start", d1, timespan.getStart());
        assertEquals("expected end", d1, timespan.getEnd());
    }
    
    @Test
    public void testGetMentionedUsersNoMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1));
        assertTrue("expected empty set", mentionedUsers.isEmpty());
    }

    @Test
    public void testGetMentionedUsersEmailIsNotMention() {
        Set<String> mentionedUsers = toLowerCase(Extract.getMentionedUsers(Arrays.asList(tweet4)));
        assertFalse("mit is not mentioned", mentionedUsers.contains("mit"));
        assertEquals("expected one user", new HashSet<>(Arrays.asList("bbitdiddle")), mentionedUsers);
    }

    @Test
    public void testGetMentionedUsersDifferentCase() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet3, tweet4));
        assertEquals("expected each user once", 2, mentionedUsers.size());
        assertEquals("expected two users", new HashSet<>(Arrays.asList("bbitdiddle", "evaluator")),
            toLowerCase(mentionedUsers));
    }

    @Test
    public void testGetMentionedUsersTwoMentions() {
        Set<String> mentionedUsers = toLowerCase(Extract.getMentionedUsers(Arrays.asList(tweet3)));
        assertEquals("expected two users", new HashSet<>(Arrays.asList("bbitdiddle", "evaluator")), mentionedUsers);
    }
    
    @Test
    public void testGetMentionedUsersSpecialCharacters() {
        Set<String> mentionedUsers = toLowerCase(Extract.getMentionedUsers(Arrays.asList(tweet5)));
        assertEquals("expected one user", new HashSet<>(Arrays.asList("cy-d-fect_2")), mentionedUsers);
    }

    private static Set<String> toLowerCase(Set<String> usernames) {
        Set<String> result = new HashSet<>();
        for (String username : usernames) {
            result.add(username.toLowerCase());
        }
        return result;
    }
}
```

### Terminal Output: `ExtractTest` Execution
```console
$ java -ea -cp "ps1/bin;ps1/lib/*" org.junit.runner.JUnitCore twitter.ExtractTest
JUnit version 4.13.2
..........
Time: 0.03

OK (10 tests)
```

### Terminal Output: `Main.java` Execution
```console
$ java -ea -cp "ps1/bin;ps1/lib/*" twitter.Main
read 8 tweets spanning [2016-02-17T10:00:00Z...2016-02-17T18:00:00Z]
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
  (7 2016-02-17T16:30:00Z alyssa) test-first programming actually saved me an hour on the PSET
```

---

## Task 2: Filtering lists of Tweets

In this task, we implemented the `writtenBy`, `inTimespan`, and `containing` methods in `Filter.java` and wrote JUnit test cases in `FilterTest.java`.

### Source Code: `Filter.java`

```java
package twitter;

import java.util.List;
import java.util.ArrayList;

public class Filter {

    public static List<Tweet> writtenBy(List<Tweet> tweets, String username) {
        List<Tweet> result = new ArrayList<>();
        for (Tweet tweet : tweets) {
            if (tweet.getAuthor().equalsIgnoreCase(username)) {
                result.add(tweet);
            }
        }
        return result;
    }

    public static List<Tweet> inTimespan(List<Tweet> tweets, Timespan timespan) {
        List<Tweet> result = new ArrayList<>();
        for (Tweet tweet : tweets) {
            if (!tweet.getTimestamp().isBefore(timespan.getStart())
                && !tweet.getTimestamp().isAfter(timespan.getEnd())) {
                result.add(tweet);
            }
        }
        return result;
    }

    public static List<Tweet> containing(List<Tweet> tweets, List<String> words) {
        List<Tweet> result = new ArrayList<>();
        for (Tweet tweet : tweets) {
            if (hasAnyWord(tweet.getText(), words)) {
                result.add(tweet);
            }
        }
        return result;
    }

    private static boolean hasAnyWord(String text, List<String> words) {
        for (String tweetWord : text.split(" ")) {
            for (String word : words) {
                if (!tweetWord.isEmpty() && tweetWord.equalsIgnoreCase(word)) {
                    return true;
                }
            }
        }
        return false;
    }
}
```

### Test Case Implementation: `FilterTest.java`

```java
package twitter;

import static org.junit.Assert.*;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import org.junit.Test;

public class FilterTest {
    
    private static final Instant d1 = Instant.parse("2016-02-17T10:00:00Z");
    private static final Instant d2 = Instant.parse("2016-02-17T11:00:00Z");
    private static final Instant d3 = Instant.parse("2016-02-17T12:00:00Z");
    
    private static final Tweet tweet1 = new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", d1);
    private static final Tweet tweet2 = new Tweet(2, "bbitdiddle", "rivest talk in 30 minutes #hype", d2);
    private static final Tweet tweet3 = new Tweet(3, "Alyssa", "Talking about the pset tonight", d3);
    
    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    
    @Test
    public void testWrittenByMultipleTweetsSingleResult() {
        List<Tweet> writtenBy = Filter.writtenBy(Arrays.asList(tweet1, tweet2), "alyssa");
        assertEquals("expected singleton list", 1, writtenBy.size());
        assertTrue("expected list to contain tweet", writtenBy.contains(tweet1));
    }

    @Test
    public void testWrittenByDifferentCaseMultipleResults() {
        List<Tweet> writtenBy = Filter.writtenBy(Arrays.asList(tweet1, tweet2, tweet3), "ALYSSA");
        assertEquals("expected two tweets in order", Arrays.asList(tweet1, tweet3), writtenBy);
    }
    
    @Test
    public void testWrittenByNoResult() {
        List<Tweet> writtenBy = Filter.writtenBy(Arrays.asList(tweet1, tweet2), "mit");
        assertTrue("expected empty list", writtenBy.isEmpty());
    }

    @Test
    public void testWrittenByEmptyList() {
        List<Tweet> writtenBy = Filter.writtenBy(Arrays.asList(), "alyssa");
        assertTrue("expected empty list", writtenBy.isEmpty());
    }
    
    @Test
    public void testInTimespanMultipleTweetsMultipleResults() {
        Instant testStart = Instant.parse("2016-02-17T09:00:00Z");
        Instant testEnd = Instant.parse("2016-02-17T12:00:00Z");
        List<Tweet> inTimespan = Filter.inTimespan(Arrays.asList(tweet1, tweet2), new Timespan(testStart, testEnd));
        assertFalse("expected non-empty list", inTimespan.isEmpty());
        assertTrue("expected list to contain tweets", inTimespan.containsAll(Arrays.asList(tweet1, tweet2)));
        assertEquals("expected same order", 0, inTimespan.indexOf(tweet1));
    }

    @Test
    public void testInTimespanEndpointsIncluded() {
        List<Tweet> inTimespan = Filter.inTimespan(Arrays.asList(tweet1, tweet2, tweet3),
            new Timespan(d2, d3));
        assertEquals("expected tweets on the endpoints", Arrays.asList(tweet2, tweet3), inTimespan);
    }

    @Test
    public void testInTimespanNoResult() {
        Timespan before = new Timespan(Instant.parse("2016-02-16T10:00:00Z"), Instant.parse("2016-02-16T20:00:00Z"));
        assertTrue("expected empty list", Filter.inTimespan(Arrays.asList(tweet1, tweet2), before).isEmpty());
    }
    
    @Test
    public void testContaining() {
        List<Tweet> containing = Filter.containing(Arrays.asList(tweet1, tweet2), Arrays.asList("talk"));
        assertFalse("expected non-empty list", containing.isEmpty());
        assertTrue("expected list to contain tweets", containing.containsAll(Arrays.asList(tweet1, tweet2)));
        assertEquals("expected same order", 0, containing.indexOf(tweet1));
    }

    @Test
    public void testContainingCaseAndWholeWords() {
        List<Tweet> containing = Filter.containing(Arrays.asList(tweet1, tweet2, tweet3), Arrays.asList("TALK"));
        assertEquals("expected tweets 1 and 2 only", Arrays.asList(tweet1, tweet2), containing);
    }

    @Test
    public void testContainingMultipleWords() {
        List<Tweet> containing = Filter.containing(Arrays.asList(tweet1, tweet2, tweet3), Arrays.asList("pset", "minutes"));
        assertEquals("expected tweets 2 and 3 in order", Arrays.asList(tweet2, tweet3), containing);
    }

    @Test
    public void testContainingNoResult() {
        List<Tweet> containing = Filter.containing(Arrays.asList(tweet1, tweet2), Arrays.asList("mit"));
        assertTrue("expected empty list", containing.isEmpty());
    }
}
```

### Terminal Output: `FilterTest` Execution
```console
$ java -ea -cp "ps1/bin;ps1/lib/*" org.junit.runner.JUnitCore twitter.FilterTest
JUnit version 4.13.2
............
Time: 0.037

OK (12 tests)
```

---

## Additional Work: SocialNetwork Analysis

### Terminal Output: `SocialNetworkTest` Execution
```console
$ java -ea -cp "ps1/bin;ps1/lib/*" org.junit.runner.JUnitCore twitter.SocialNetworkTest
JUnit version 4.13.2
......
Time: 0.015

OK (6 tests)
```

### Terminal Output: All Tests Combined Execution
```console
$ java -ea -cp "ps1/bin;ps1/lib/*" org.junit.runner.JUnitCore twitter.ExtractTest twitter.FilterTest twitter.SocialNetworkTest
JUnit version 4.13.2
............................
Time: 0.057

OK (28 tests)
```
