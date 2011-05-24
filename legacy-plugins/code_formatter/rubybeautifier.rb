#!/usr/bin/env ruby
# http://blog.neontology.com/articles/2006/05/10/beautiful-ruby-in-textmate
# http://www.arachnoid.com/ruby/rubyBeautifier.html
#
# Ruby beautifier, version 1.3, 04/03/2006
# Copyright (c) 2006, P. Lutus
# TextMate modifications by T. Burks
# Vim modifications by Luis Mondesi
# Released under the GPL

$tabSize = 2
$tabStr = " "

# indent regexp tests

$indentExp = [
   /^module\b/,
   /(=\s*|^)if\b/,
   /(=\s*|^)until\b/,
   /(=\s*|^)for\b/,
   /(=\s*|^)unless\b/,
   /(=\s*|^)while\b/,
   /(=\s*|^)begin\b/,
   /(=\s*|^)case\b/,
   /\bthen\b/,
   /^class\b/,
   /^rescue\b/,
   /^def\b/,
   /\bdo\b/,
   /^else\b/,
   /^elsif\b/,
   /^ensure\b/,
   /\bwhen\b/,
   /\{[^\}]*$/,
   /\[[^\]]*$/
]

# outdent regexp tests

$outdentExp = [
   /^rescue\b/,
   /^ensure\b/,
   /^elsif\b/,
   /^end\b/,
   /^else\b/,
   /\bwhen\b/,
   /^[^\{]*\}/,
   /^[^\[]*\]/
]

def makeTab(tab)
   return (tab < 0)?"":$tabStr * $tabSize * tab
end

def addLine(line,tab)
   line.strip!
   line = makeTab(tab)+line if line.length > 0
   return line + "\n"
end

def beautifyRuby
   commentBlock = false
   multiLineArray = Array.new
   multiLineStr = ""
   tab = 0
   source = STDIN.read
   dest = ""
   source.split("\n").each do |line|
      # combine continuing lines
      if(!(line =~ /^\s*#/) && line =~ /[^\\]\\\s*$/)
         multiLineArray.push line
         multiLineStr += line.sub(/^(.*)\\\s*$/,"\\1")
         next
      end

      # add final line
      if(multiLineStr.length > 0)
         multiLineArray.push line
         multiLineStr += line.sub(/^(.*)\\\s*$/,"\\1")
      end

      tline = ((multiLineStr.length > 0)?multiLineStr:line).strip
      if(tline =~ /^=begin/)
         commentBlock = true
      end
      if(commentBlock)
         # add the line unchanged
         dest += line + "\n"
      else
         commentLine = (tline =~ /^#/)
         if(!commentLine)
            # throw out sequences that will
            # only sow confusion
            tline.gsub!(/\/.*?\//,"")
            tline.gsub!(/%r\{.*?\}/,"")
            tline.gsub!(/%r(.).*?\1/,"")
            tline.gsub!(/\\\"/,"'")
            tline.gsub!(/".*?"/,"\"\"")
            tline.gsub!(/'.*?'/,"''")
            tline.gsub!(/#\{.*?\}/,"")
            $outdentExp.each do |re|
               if(tline =~ re)
                  tab -= 1
                  break
               end
            end
         end
         if (multiLineArray.length > 0)
            multiLineArray.each do |ml|
               dest += addLine(ml,tab)
            end
            multiLineArray.clear
            multiLineStr = ""
         else
            dest += addLine(line,tab)
         end
         if(!commentLine)
            $indentExp.each do |re|
               if(tline =~ re && !(tline =~ /\s+end\s*$/))
                  tab += 1
                  break
               end
            end
         end
      end
      if(tline =~ /^=end/)
         commentBlock = false
      end
   end
   STDOUT.write(dest)
   # uncomment this to complain about mismatched blocks
   #if(tab != 0)
   #  STDERR.puts "Indentation error: #{tab}"
   #end 
end

beautifyRuby 
