exec java -da -Xmx1G -XX:MaxPermSize=256m -classpath ./prom/source/ProM66.jar -Djava.util.Arrays.useLegacyMergeSort=true org.processmining.contexts.cli.CLI $1 $2
