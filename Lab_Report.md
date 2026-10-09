# Lab 5 - Test First Programming

## Project Configuration
The initial IDE configuration problems related to the Java build path (`java.lang.invoke.StringConcatFactory` error) have been successfully resolved by updating the `.classpath` file to use the default system JRE container instead of a restrictive JavaSE-1.8 container.

## Task 1: SocialNetwork Implementation and Testing

### 1.1 Source Code Implementation (`SocialNetwork.java`)

```java
    public static Map<String, Set<String>> guessFollowsGraph(List<Tweet> tweets) {
        Map<String, Set<String>> graph = new java.util.HashMap<>();
        for (Tweet tweet : tweets) {
            String author = tweet.getAuthor().toLowerCase();
            if (!graph.containsKey(author)) {
                graph.put(author, new java.util.HashSet<>());
            }
            Set<String> mentioned = Extract.getMentionedUsers(java.util.Collections.singletonList(tweet));
            for (String user : mentioned) {
                if (!user.equals(author)) {
                    graph.get(author).add(user);
                }
            }
        }
        return graph;
    }

    public static List<String> influencers(Map<String, Set<String>> followsGraph) {
        Map<String, Integer> followerCounts = new java.util.HashMap<>();
        
        for (String user : followsGraph.keySet()) {
            if (!followerCounts.containsKey(user)) {
                followerCounts.put(user, 0);
            }
            for (String followed : followsGraph.get(user)) {
                followerCounts.put(followed, followerCounts.getOrDefault(followed, 0) + 1);
            }
        }
        
        List<String> result = new java.util.ArrayList<>(followerCounts.keySet());
        result.sort((u1, u2) -> followerCounts.get(u2).compareTo(followerCounts.get(u1)));
        return result;
    }
```

### 1.2 Test Cases Implementation (`SocialNetworkTest.java`)

```java
    /*
     * Testing strategy for guessFollowsGraph:
     *   tweets list: empty, size 1, size > 1
     *   mentions in tweets: 0, 1, > 1
     *   authors: distinct, same author multiple tweets
     *   mentions case insensitivity
     * 
     * Testing strategy for influencers:
     *   followsGraph: empty, size 1, size > 1
     *   follower counts: all 0, distinct counts, tie in counts
     */
    
    @Test
    public void testGuessFollowsGraphEmpty() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<>());
        assertTrue("expected empty graph", followsGraph.isEmpty());
    }

    @Test
    public void testGuessFollowsGraphSingleTweetNoMentions() {
        Tweet tweet = new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", java.time.Instant.now());
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(java.util.Arrays.asList(tweet));
        assertTrue("expected graph with alyssa mapping to empty set", followsGraph.containsKey("alyssa"));
        assertTrue("expected empty set for alyssa", followsGraph.get("alyssa").isEmpty());
    }

    @Test
    public void testGuessFollowsGraphMultipleMentions() {
        Tweet tweet = new Tweet(1, "alyssa", "@bbitdiddle and @carl", java.time.Instant.now());
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(java.util.Arrays.asList(tweet));
        assertTrue("expected graph with alyssa", followsGraph.containsKey("alyssa"));
        assertTrue("expected alyssa to follow bbitdiddle", followsGraph.get("alyssa").contains("bbitdiddle"));
        assertTrue("expected alyssa to follow carl", followsGraph.get("alyssa").contains("carl"));
    }
    
    @Test
    public void testInfluencersEmpty() {
        Map<String, Set<String>> followsGraph = new HashMap<>();
        List<String> influencers = SocialNetwork.influencers(followsGraph);
        assertTrue("expected empty list", influencers.isEmpty());
    }

    @Test
    public void testInfluencersMultipleUsers() {
        Map<String, Set<String>> followsGraph = new HashMap<>();
        followsGraph.put("alyssa", new java.util.HashSet<>(java.util.Arrays.asList("bbitdiddle", "carl")));
        followsGraph.put("bbitdiddle", new java.util.HashSet<>(java.util.Arrays.asList("carl")));
        followsGraph.put("carl", new java.util.HashSet<>());
        
        List<String> influencers = SocialNetwork.influencers(followsGraph);
        
        assertEquals("expected size 3", 3, influencers.size());
        assertEquals("expected carl first", "carl", influencers.get(0));
        assertEquals("expected bbitdiddle second", "bbitdiddle", influencers.get(1));
        assertEquals("expected alyssa third", "alyssa", influencers.get(2));
    }
```

### 1.3 Test Output and Result Screenshots

After implementing the solutions, the test suite executes successfully when run with assertions enabled:

```text
JUnit version 4.13.2
............................
Time: 0.057

OK (28 tests)
```

**JUnit Tests Passing (Screenshot)**
![All Tests Passed](file:///e:/Semester%205/Labs/SC/lab5SC/all_pass.png)

**Extract Passing Tests**
![Extract Pass](file:///e:/Semester%205/Labs/SC/lab5SC/extract_pass.png)

**Filter Passing Tests**
![Filter Pass](file:///e:/Semester%205/Labs/SC/lab5SC/filter_pass.png)

### 1.4 Main.java Execution Output

```text
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

**Main Execution Output (Screenshot)**
![Main Execution](file:///e:/Semester%205/Labs/SC/lab5SC/main_output.png)
