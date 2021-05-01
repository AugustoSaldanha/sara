async function search() {
    try {
	// get all parameters
        const TorrentIndexer = require("torrent-indexer"); //need of torrent indexer to seach a torrent file
        const torrentIndexer = new TorrentIndexer();
	const mediaName = process.argv[2];
	const mediaSeason = parseInt(process.argv[4]);
	const mediaEpisode = parseInt(process.argv[5]);
	let   mediaType = process.argv[3];

	// define if is a Movie, Serie or Anime
	switch (mediaType){
            case 'Serie':
                mediaType = "series";
                break;
            case 'Filme':
                mediaType = "movie";
                break;
            case 'Anime':
                mediaType = "anime";
                break;
            default:
                mediaType = null;
	}

        const torrents = await torrentIndexer.search(mediaName, mediaType);// Now de magic...

	var media = [];
	let seed = 10;

        torrents.forEach(torrent => {
	    if (torrent.link != undefined){
                if (torrent.link.match(/magnet/) ){
                    if (mediaType === "series" || mediaType === "anime"){
                        if(torrent.season === mediaSeason && torrent.episode === mediaEpisode) {
                            if (torrent.seeders > seed){
                                media = torrent;
                                seed = torrent.seeders;
			    }
		        }
		    }else {
                        if (torrent.seeders > seed) {
                            media = torrent;
                            seed = torrent.seeders;
		        }
		    } 
                }
	    }
	});
    console.log(media);
    }catch{console.log("Sorry, something is wrong"); }
}

search();
