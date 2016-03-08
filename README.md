# tissue

your project's issue tracker, in a text file

## How it (will) work  

You write your issues in a local file (markdown / restructuredtext). Each section is an issue (starting level configurable). 
At the top or bottom you can add metadata: Online id, status, tags, milestone, etc. 

Tissue should be able to synchronize this issues with your issue tracker. Github as first target. Bitbucket next. Others? 


## What we need. 

- models: classes that represent "issues" and it related metadata. 
- Parser: this is the component that know how to parse the file an create modes instances
- API manager/s: they know how to fetch issue tracker data and send it back online.   









