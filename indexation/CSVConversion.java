package csvConversion;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Scanner;

public class CSVConversion {
	
	public static void main(String[] args) throws Exception {		
		System.out.println("Test conversion...");
		CSVConversion.conversion();
	}

	public static void conversion() throws Exception {

		try {
			
			// On crée le nouveau fichier de texte
			File result = new File("/home/nikita/Documents/data-elasticsearch/result.csv");
			
			FileWriter fw = new FileWriter (result);
			BufferedWriter bw = new BufferedWriter (fw);
			PrintWriter out = new PrintWriter (bw);

			File dir = new File("/media/nikita/NikitaDD/text");
			File[] years = dir.listFiles();

			if (years != null) {
				for (File child : years) {

					String year = child.getName();

					System.out.println("Année : " + year);

					File[] months = child.listFiles();
					if (months != null) {
						for (File littlechild : months) {

							String month = littlechild.getName();
							
							System.out.println("Mois : " + month);

							File[] days = littlechild.listFiles();
							if (days != null) {
								for (File verylittlechild : days) {

									String day = verylittlechild.getName();
									
									System.out.println("Jour : " + day);
									
									//File dir1 = new File("/home/nikita/Documents/data-elasticsearch/"+ year + "/" + month + "/" + day);

									File[] articles = verylittlechild.listFiles();
									if (articles != null /* && dir1.mkdirs()*/) {
										for (File art : articles) {

											String nom = art.getName();
										
											Scanner s1 = new Scanner(art);
											s1.useDelimiter("\\s*\n\\s*");
											
											// Recherche de l'ID
											String id = nom.split("_")[1].split(".t")[0];
											
											System.out.println("Article : " + nom + " ID : " + id);
																						
											out.print(year + "-" + month + "-" + day + ";!");
											
											// Ecriture de l'ID
											out.print(id + ";!");
																						
											// Ecriture des lignes
											while (s1.hasNext()){
												out.print(s1.next() + "\t"); 
											}
											
											out.println();
											s1.close();
											
											System.out.println("Fin !");

										}
									} else {
										System.out.println("articles != null");
									}

								}
							} else {
								System.out.println("days != null");
							}

						}
					} else {
						System.out.println("months != null");
					}

				}
			} else {
				System.out.println("years != null");
			}
			out.close();
		}
		catch (Exception e){
			System.out.println(e.toString());
		}
	}
}
