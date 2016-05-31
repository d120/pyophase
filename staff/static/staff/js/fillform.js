function fillform(){
	if(window.location.hash) {
		var hash = window.location.hash;

		// prefix for fillform of the hash
		var prefix = '#fillform&v=1';

		// the given id prefix of Django
		var idprefix = 'id_'

		// does the hash contain fillform information?
		if (hash.substring(0, prefix.length ) == prefix){
			// array of allowed model fields to fill
			var allowed_keys=['prename','name','email','phone',
			                  'matriculated_since', 'degree_course',
			                  'experience_ophase', 'why_participate',
			                  'remarks']
			// split hash value by & into an array
			var pieces = hash.split('&');

			for (var i = 0; i < pieces.length; i++){
				var cur = pieces[i];

				// each element is key = value.
				// if ther is a another = it part of the value
				var arr = cur.split('=', 2);
				var key = arr[0];
				var value = decodeURIComponent(arr[1]);


				//is the key allowed for fillform?
				if (allowed_keys.indexOf(key) > -1){
					document.getElementById(idprefix + key).value = value;
				}
			}
		}
	}
}
