/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

public class SocialNetworkTest {

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
    
    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    
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

    /*
     * Warning: all the tests you write here must be runnable against any
     * SocialNetwork class that follows the spec. It will be run against several
     * staff implementations of SocialNetwork, which will be done by overwriting
     * (temporarily) your version of SocialNetwork with the staff's version.
     * DO NOT strengthen the spec of SocialNetwork or its methods.
     * 
     * In particular, your test cases must not call helper methods of your own
     * that you have put in SocialNetwork, because that means you're testing a
     * stronger spec than SocialNetwork says. If you need such helper methods,
     * define them in a different class. If you only need them in this test
     * class, then keep them in this test class.
     */

}
