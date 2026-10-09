package twitter;


import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        final boolean assertsEnabled = Main.class.desiredAssertionStatus();
        if (!assertsEnabled) {
            throw new Error("Always run main and tests with assertions enabled");
        }
        
        List<Tweet> tweets = Arrays.asList(
            new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", Instant.parse("2016-02-17T10:00:00Z")),
            new Tweet(2, "bbitdiddle", "rivest talk in 30 minutes #hype", Instant.parse("2016-02-17T11:00:00Z")),
            new Tweet(3, "alyssa", "@bbitdiddle saving you a seat in 32-123", Instant.parse("2016-02-17T11:20:00Z")),
            new Tweet(4, "evaluator", "thanks @BBitDiddle! mail me at eval@mit.edu", Instant.parse("2016-02-17T12:00:00Z")),
            new Tweet(5, "cy_d_fect", "anyone started pset 1 yet? mail me at cy@mit.edu", Instant.parse("2016-02-17T13:40:00Z")),
            new Tweet(6, "someone", "look at @cy_d_fect!", Instant.parse("2016-02-17T15:00:00Z")),
            new Tweet(7, "alyssa", "test-first programming actually saved me an hour on the PSET", Instant.parse("2016-02-17T16:30:00Z")),
            new Tweet(8, "alyssa", "@alyssa @rivest we should talk more", Instant.parse("2016-02-17T18:00:00Z"))
        );
        
        Timespan span = Extract.getTimespan(tweets);
        System.out.println("read " + tweets.size() + " tweets spanning [" + span.getStart() + "..." + span.getEnd() + "]");
        
        Set<String> mentionedUsers = Extract.getMentionedUsers(tweets);
        System.out.println("mentioned users: " + mentionedUsers);
        
        System.out.println("tweets written by alyssa:");
        for (Tweet t : Filter.writtenBy(tweets, "alyssa")) {
            System.out.println("  (" + t.getId() + " " + t.getTimestamp() + " " + t.getAuthor() + ") " + t.getText());
        }
        
        System.out.println("tweets containing 'rivest' or 'pset':");
        for (Tweet t : Filter.containing(tweets, Arrays.asList("rivest", "pset"))) {
            System.out.println("  (" + t.getId() + " " + t.getTimestamp() + " " + t.getAuthor() + ") " + t.getText());
        }
    }
}
