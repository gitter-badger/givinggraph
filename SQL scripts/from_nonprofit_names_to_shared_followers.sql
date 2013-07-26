SELECT weight as shared_followers 
FROM giving.nonprofit_twitter_edges as edges, giving.nonprofits as non1, giving.nonprofits as non2
WHERE non1.name = 'XXX' and non2.name = 'XXX' and
	(edges.source = non1.twitter_name and edges.target = non2.twitter_name or
	edges.source = non2.twitter_name and edges.target = non1.twitter_name)
			