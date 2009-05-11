#!/usr/bin/perl -w

$f1 = "mappedX";
$f2 = "../words.asc";
open(F1, "<$f1");
open(F2, "<$f2");
while(<F1>) {
    $a = $_;
    $b = <F2>;
    chop $b;
    print "$b $a";
}
