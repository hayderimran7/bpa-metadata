#!/usr/bin/env python
# coding: utf-8

# q&d for paula
# swift list Wheat_Pathogens -p processed | ./processed.py > index.html

import fileinput

html = """<!DOCTYPE html>
<html>
  <head>
    <title>BASE | BioPlatforms Australia Data Access</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8" />
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <style>
    .content-div {
      padding-left: 1em;
      padding-right: 1em;
    }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-default" role="navigation">
      <!-- Brand and toggle get grouped for better mobile display -->
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="/">Bioplatforms Australia Downloads</a>
      </div>
    </nav>

    <div class="content-div">
       <table id="listing">
       <tr id="heading">
        <th class="colname">Wheat Fungal Pathogens Release V1.0</th>
       </tr>

       {TABLE_CONTENT}

    </div>

    <script src="//code.jquery.com/jquery.min.js"></script><script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>

    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-45275056-1', 'bioplatforms.com');
      ga('send', 'pageview');
    </script>

    <form><input type="hidden" id="bpam-catalog" value="melanoma" /></form>
  </body>
</html>


"""


def make_section(link, name):
    tr_template = """
     <tr class="item type-application type-octet-stream">
        <td class="colname"><a href="http://swift.bioplatforms.com/v1/AUTH_b154c0aff02345fba80bd118a54177ea/Wheat_Pathogens/{0}">{1}</a></td>
     </tr>
    """.format(link, name)

    return tr_template


if __name__ == "__main__":
    table = []
    for line in fileinput.input():
        line = line.strip()
        parts = line.split('/')
        table.append(make_section(line, parts[-1]))

    table_content = "\n".join(table)
    html = html.replace('{TABLE_CONTENT}', table_content)

    print html


