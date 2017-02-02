// command to run
// javac -cp . lab1/NaiveBayes.java 
// java lab1/NaiveBayes ../20newsgroups/vocabulary.txt ../20newsgroups/map.csv ../20newsgroups/train_label.csv ../20newsgroups/train_data.csv ../20newsgroups/test_label.csv ../20newsgroups/test_data.csv

package lab1;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.NotActiveException;
import java.util.Scanner;

public class NaiveBayes {
	
	static final Integer num_documents  = 18824;
	static final Integer num_train_data = 11269;
	static final Integer num_test_data  = 7505;
	static final Integer num_vocabulary = 61188;
	static final Integer num_category   = 20;

	public static void main(String[] args) throws FileNotFoundException, InterruptedException {
		// TODO Auto-generated method stub
		String vocabulary  = args[0];
		String map_csv     = args[1];
		String train_label = args[2];
		String train_data  = args[3];
		String test_label  = args[4];
		String test_data   = args[5];
		// train variables
		HashMap<Integer, Integer> prior_train          = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> doc_to_news_train    = new HashMap<Integer, Integer>();
		HashMap<Integer, Word> news_to_word_train	   = new HashMap<Integer, Word>();
		// test variables
		HashMap<Integer, Integer> prior_test 	       = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> doc_to_news_test     = new HashMap<Integer, Integer>();
		HashMap<Integer, Word> news_to_word_test	   = new HashMap<Integer, Word>();
		
		//* 2.1 Learn naive bayes model
		
		/////////////////////////////////////////////////////////////////////////////////////
		// train data
		List<HashMap<Integer,Integer>> dictionaryList_train = new ArrayList<HashMap<Integer,Integer>>();
		dictionaryList_train = prior_probability(train_label);
		
		prior_train          = dictionaryList_train.get(0);
		doc_to_news_train    = dictionaryList_train.get(1);
		
		news_to_word_train   = calculate_words(doc_to_news_train, train_data);
		
		// from the above info, calculate the class prior
		HashMap<Integer, Float> P_prior_train = new HashMap<Integer, Float>();
		P_prior_train 					      = calculate_prior(prior_train,num_train_data);
		// testing this
//		for (int i : P_prior_train.keySet())
//		{
//			System.out.println("P(Omega = "+ String.valueOf(i)+") = "+String.valueOf(P_prior_train.get(i)));
//		}
		//calculate the MLE for each word in each newsgroup
		HashMap<Integer, List<Float>> MLE_prior_train = new HashMap<Integer, List<Float>>();
		MLE_prior_train  							  = calculate_MLE(news_to_word_train);
		
		//calculate the BE for each word in each newsgroup
		HashMap<Integer, List<Float>> BE_prior_train = new HashMap<Integer, List<Float>>();
		
		BE_prior_train								 = calculate_BE(news_to_word_train);
		
		
		/////////////////////////////////////////////////////////////////////////////////////
		// test data
		// initiate our news_to_word
//		List<HashMap<Integer,Integer>> dictionaryList_test = new ArrayList<HashMap<Integer,Integer>>();
//		dictionaryList_test  = prior_probability(test_label);
//		prior_test 			 = dictionaryList_test.get(0);
//		doc_to_news_test	 = dictionaryList_test.get(1);
//		news_to_word_test    = calculate_words(doc_to_news_test, test_data);
//		// from the above info, calculate the class prior
//		HashMap<Integer, Float> P_prior_test = new HashMap<Integer, Float>();
//		P_prior_test 					     = calculate_prior(prior_train,num_train_data);
//		
//		//calculate the MLE for each word in each newsgroup
//		HashMap<Integer, List<Float>> MLE_prior_test = new HashMap<Integer, List<Float>>();
//		MLE_prior_test  							 = calculate_MLE(news_to_word_test);
//		//calculate the BE for each word in each newsgroup
//		HashMap<Integer, List<Float>> BE_prior_test = new HashMap<Integer, List<Float>>();
//		BE_prior_test  							    = calculate_MLE(news_to_word_test);
		
		
		//* 2.2
		// train data
		// dictionary, key is doc_id, key is a word object (has word_id as key, count of word as value)
		
		HashMap<Integer, Word_reduce> doc_to_word_train    = new HashMap<Integer, Word_reduce>();
		doc_to_word_train						    = document_to_word(train_data, num_train_data);

		// dictionary, key is news_id, value is list of float value (20 of them represents 20 categories)
		HashMap<Integer, Integer> doc_to_news_nb_train = new HashMap<Integer, Integer>();
		doc_to_news_nb_train						   = find_BE_each_doc(BE_prior_train, doc_to_word_train, P_prior_train, num_test_data);
		// test
//		for (Integer i: news_nb_train.keySet())
//		{	
//			System.out.println("document "+ String.valueOf(i)+" is of new class "
//		+String.valueOf(news_nb_train.get(i)));
//		}
		//** 2.2.1 compute overall accuracy using news_nb_train, and doc_to_news_train
		Float overall_accuracy = calculate_overall_accuracy(doc_to_news_nb_train, doc_to_news_train, num_train_data);
		System.out.println("Overall Accuracy is:"+Float.toString(overall_accuracy));
		
		// using doc_to_news_nb_train, and doc_to_news_train, create 2 dictionaries that map each classification
		// to an array of document ids.
		HashMap<Integer, List<Integer>> new_to_doc_train = convert_new_to_docs(doc_to_news_train);
		HashMap<Integer, List<Integer>> new_to_doc_nb    = convert_new_to_docs(doc_to_news_nb_train);
		System.out.println("Class accuracy:");
		for (int news_id: new_to_doc_train.keySet())
		{
			int size 				  = new_to_doc_train.size();
			int found_count 		  = 0;
			List<Integer> nb_array    = new_to_doc_nb.get(news_id);
			List<Integer> train_array = new_to_doc_train.get(news_id);
			for (int i=0;i<nb_array.size();i++)
			{
				if (train_array.contains(nb_array.get(i)))
					{
					found_count +=1;
					}
			}
			System.out.println("Group "+String.valueOf(news_id)+":  "+Float.toString((float) found_count/size));
					
		}
		
		// test data
//		HashMap<Integer, Word> doc_to_word_test  = new HashMap<Integer, Word>();
//		doc_to_word_test						 = document_to_word(train_data, num_train_data);
		
	}
	////////////////////////////////////////////////////////////
	// functions
	
	// function that take in label.csv 
	// return an array of 2 
	// first dic is prior dic: key is newsid, value is number of doc assigned as newsid
	// second dic is doc_to_news: key is docid, value is the assigned newsid
	public static List<HashMap<Integer, Integer>> prior_probability (String file_label) throws FileNotFoundException{
		List<HashMap<Integer,Integer>> dictionaryList = new ArrayList<HashMap<Integer,Integer>>();
		HashMap<Integer, Integer> prior = new HashMap<Integer, Integer>();
		HashMap<Integer, Integer> doc_to_news = new HashMap<Integer, Integer>();
		File csv = new File(file_label);
		Scanner my_scanner = new Scanner(csv);
		int doc_id = 1;
		while (my_scanner.hasNext())
		{
			String line    = my_scanner.next();
			// split it by ",", label is in format of "newgroup ids"
			String[] info  = line.split(",");
			int news_id  = Integer.parseInt(info[0]);		
			doc_to_news.put(doc_id, news_id);
			if (prior.containsKey(news_id))
			{
				prior.put(news_id, prior.get(news_id)+1);
			}
			else
			{
				prior.put(news_id, 1);
			}
			doc_id+=1;
		}
		my_scanner.close();
		dictionaryList.add(prior);
		dictionaryList.add(doc_to_news);
		return dictionaryList;
	}
	// method that given data.csv, create a dictionary
	// key is the words id, value is a word object
	public static HashMap<Integer, Word_reduce> document_to_word(String file_data, int num_doc) throws FileNotFoundException
	{
		HashMap<Integer, Word_reduce> doc_to_word = new HashMap<Integer, Word_reduce>();
		for (int i =1; i<=num_doc; i++)
		{
			// System.out.println("Initiating word_reduce object for doc "+String.valueOf(i));
			Word_reduce word = new Word_reduce(); // using word_reduce to reduce memory usage
			doc_to_word.put(i, word);
		}
		File csv = new File(file_data);
		Scanner my_scanner = new Scanner(csv);
		while (my_scanner.hasNext())
		{
			String line   = my_scanner.next();
			// System.out.println("Current line:"+line);
			String[] info = line.split(",");
			int doc_id    = Integer.parseInt(info[0]);
			int word_id   = Integer.parseInt(info[1]);
			int count	  = Integer.parseInt(info[2]);
			// use the above 2 info, update our Word object
			doc_to_word.get(doc_id).update(word_id, count);
		}
		my_scanner.close();
		return doc_to_word;
	}
	
	// method that given doc_to_news dictionary
	// and the data.csv provide a dictionary: key is the newsid, value: word object
	public static HashMap<Integer, Word> calculate_words(HashMap<Integer, Integer> doc_to_news, String file_data) throws FileNotFoundException
	{
		HashMap<Integer, Word> news_to_word = new HashMap<Integer, Word>();
		// initiate our news_to_word
		for (int i =1; i<=num_category; i++)
		{
			Word word = new Word(num_vocabulary);
			news_to_word.put(i, word);
		}
		File csv = new File(file_data);
		Scanner my_scanner = new Scanner(csv);
		while (my_scanner.hasNext())
		{
			String line   = my_scanner.next();
			String[] info = line.split(",");
			int doc_id    = Integer.parseInt(info[0]);
			// pull data from the doc_to_news to know which news this doc is classified to
			int news_id   = doc_to_news.get(doc_id);
			int word_id   = Integer.parseInt(info[1]);
			int count	  = Integer.parseInt(info[2]);
			// use the above 2 info, update our Word object
			news_to_word.get(news_id).update(word_id, count);
		}
		return news_to_word;
	}
	// calculate the prior probability
	public static HashMap<Integer, Float> calculate_prior(HashMap<Integer, Integer> prior, int num_data)
	{
		HashMap<Integer, Float> P_prior =  new HashMap<Integer, Float>();
		for (Integer new_id: prior.keySet())
		{		
			P_prior.put(new_id, (float) prior.get(new_id)/num_data);
		}
		return P_prior;
	}
	
	// calculate the MLE probability
	public static HashMap<Integer, List<Float>> calculate_MLE(HashMap<Integer, Word> news_to_word)
	{
		HashMap<Integer, List<Float>> MLE_prior =  new HashMap<Integer, List<Float>>();
		for (Integer new_id: news_to_word.keySet())
		{
			List<Float> MLE = new ArrayList<Float>(); // store MLE for each word for each new_id
			Word word = news_to_word.get(new_id); // get the word object
			// get the total number of words in all document in class new_id
			Integer n = word.total_count;
			// iterate through the word_id in the word_dic
			for (Integer word_id: word.word_dic.keySet())
			{
				MLE.add((float) word.word_dic.get(word_id)/n);
			}
			MLE_prior.put(new_id, MLE);
		}
		return MLE_prior;
	}
	
	// calculate the BE probability
	public static HashMap<Integer, List<Float>> calculate_BE(HashMap<Integer, Word> news_to_word)
	{
		HashMap<Integer, List<Float>> BE_prior =  new HashMap<Integer, List<Float>>();
		for (Integer new_id: news_to_word.keySet())
		{
			List<Float> BE = new ArrayList<Float>(); // store MLE for each word for each new_id
			Word word = news_to_word.get(new_id); // get the word object
			// get the total number of words in all document in class new_id
			Integer n = word.total_count;
			// iterate through the word_id in the word_dic
			for (Integer word_id: word.word_dic.keySet())
			{
				BE.add((float) (word.word_dic.get(word_id)+1)/(n+num_vocabulary));
			}
			BE_prior.put(new_id, BE);
		}
		return BE_prior;
	}
	// calculate the naive baye classifier value for each category for each document
	// input: doc_to_word dictionary, BE_prior dictionary, P_prior, num_doc
	// output: news_nb dictionary
	public static HashMap<Integer, Integer> find_BE_each_doc (HashMap<Integer, List<Float>> BE_prior
			, HashMap<Integer, Word_reduce> doc_to_word, HashMap<Integer, Float> P_prior, int num_doc)
	{
		HashMap<Integer, Integer> news_nb = new HashMap<Integer, Integer>();
		// iterate through each category
		for (int doc_id = 1; doc_id <=num_doc; doc_id++ )
		{
			List<Float> NB = new ArrayList<Float>(); // list of float of naive bayes
			for (int news_id=1;news_id<=20;news_id++)
			{
				Float prior = (float) Math.log(P_prior.get(news_id)); // get the prior probabilty of class wj
				// get the word_dic from the Word object of the doc_to_word
				Word_reduce word   = doc_to_word.get(doc_id);
				for (int word_id: word.word_dic.keySet())
				{	
					Float value    = (float) word.word_dic.get(word_id);
					Float BE_value = BE_prior.get(news_id).get(word_id-1);
					if (BE_value > 0)
					{
						prior += value* (float) Math.log(BE_prior.get(news_id).get(word_id-1));
					}
					else
					{
						prior =(float) Double.NEGATIVE_INFINITY;
						break;
					}
					
				}
				// add this new NB value of float into the NB array
				NB.add(prior);
			}
			// find max in the NB array
			float maximum = Collections.max(NB);
			int index     = NB.indexOf(maximum)+1; // get the index
			news_nb.put(doc_id, index);
		}
		return news_nb;
	}
	
	public static Float calculate_overall_accuracy(HashMap<Integer, Integer> news_nb,
			HashMap<Integer, Integer> doc_to_news, int num_data)
	{
		int wrong_count = 0;
		float result;
		for (int doc_id: news_nb.keySet())
		{
			if (news_nb.get(doc_id) != (doc_to_news.get(doc_id)))
			{
				wrong_count +=1;
			}
		}
		result = (float) wrong_count/num_data;
		return 1-result;
	}
	// given a dictionary in form of key as doc_id, value is news_id
	// reverse it into key is news_id, value is array of doc_ids
	public static HashMap<Integer, List<Integer>> convert_new_to_docs(HashMap<Integer, Integer> doc_to_news)
	{
		HashMap<Integer, List<Integer>> result = new HashMap<Integer, List<Integer>>();
		for (int doc_id: doc_to_news.keySet())
		{
			int news_id = doc_to_news.get(doc_id);
			if (result.containsKey(news_id))
			{
				result.get(news_id).add(doc_id);
			}
			else 
			{
				List<Integer> local = new ArrayList<Integer>();
				local.add(doc_id);
				result.put(news_id, local);
			}
		}
		return result;
	}
}
//////////////////////////////////////////////////////////////////////////////////////////
// helper classes
// class word that store a hashtable that key is  the word id and value it is its count
class Word{
	HashMap<Integer, Integer> word_dic = new HashMap<Integer, Integer>();
	int total_count = 0;
	public Word(int num_vocab) 
	{
		int i;
		for (i =1;i<=num_vocab;i++)
		{
			word_dic.put(i, 0);//initiate the key of word, and value as 0
		}
	}
	public void update(int id, int new_count) {
		word_dic.put(id, word_dic.get(id)+new_count);
		total_count += new_count;
	}
}

class Word_reduce
{
	HashMap<Integer, Integer> word_dic = new HashMap<Integer, Integer>();
	int total_count = 0;
	public Word_reduce()
	{
		
	}
	public void update(int id, int new_count) {
		total_count += new_count;
		if (word_dic.containsKey(id))
		{
			word_dic.put(id, word_dic.get(id)+new_count);
		}
		else 
		{
			word_dic.put(id, new_count);
		}
	}
}
