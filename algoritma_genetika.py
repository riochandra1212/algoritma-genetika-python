import numpy as np
import math 
import random

class Algoritma_genetika:
	# membuat algoritma genetika
	# misalkan ada persamaan a+2b+3c+4d = 30
	# maka buat algoritma genetika untuk mencari nilai a,b,c, dan d

	jumlah_chrom = 10 #jumlah chromosome
	gen = ["a", "b", "c", "d"] #nilai gen abcd
	nilai_per_gen = {
		'min' : 0,
		'max' : 30
	} #nilai per gen 0-30\
	crossover_rate = 50/100 #persen
	mutasi_rate = 50/100 #persen
	total_generasi = 1000
	next_gen = np.arange(4)
	stop = False
	def __init__(self):
		#pembentukan choromosome random
		self.first_chromosome = np.random.randint(low=self.nilai_per_gen['min'], high=self.nilai_per_gen['max'], size=(self.jumlah_chrom, len(self.gen)))
		print(self.first_chromosome)
		print("==========================================")
		print("==========================================")
		print("==========================================")
		

	def evaluasi_chrom(self, chrom, generasi):
		#evaluasi chromosome
		#hitung fungsi_objektif dari chromosome yang telah dibuat
		# fungsi_objektif(chromosome) = | (a+2b+3c+4d) – 30 |
		# 
		print("GENERASI ["+str(generasi)+"] ----------------------")
		
		jumlah_chromo = len(chrom)
		j = np.arange(jumlah_chromo)   
		fitness = np.arange(jumlah_chromo, dtype='f')
		
		for x in range(len(chrom)):
			
			#FUNGSI OBJEKTIF 
			ev = abs((chrom[x][0]+2*chrom[x][1]+3*chrom[x][2]+4*chrom[x][3])-30)
			j[x] = ev
			
			#SELEKSI CHROMOSOME, DAN MENCARI FITNESS
			fitn = 1/(ev+1)
			
			fitness[x] = fitn
			if(fitn == 1):
				self.stop = True
			print("CHROMOSOME {0} : {1}, fitness = {2}".format(x, np.array2string(chrom[x], separator=','), fitn))
		print("FITNESS DONE")
		print(j)
		
		#cari PROBABILITAS (P)
		P = np.arange(jumlah_chromo, dtype='f')
		# print(fitness)
		total_fitness = fitness.sum()
		P = fitness / total_fitness
		print("total fitness : {}".format(str(total_fitness)))
		print("Rata-rata fitness : {}".format(str(np.average(fitness))))
		print("Probabilitas : {}".format(np.array2string(P, separator=',')))
		print("pobabilitas PALING TINGGI : {}, pada chromosome {}".format(P[P.argmax()], str(P.argmax())))
		print("CHOROMSOME YANG MUNGKIN TERPILIH : {}".format(np.array2string(chrom[P.argmax()], separator=',')))
		self.next_gen = chrom[P.argmax()]
		#seleksi dengan ROULETE WHELL (C) cumulative probabilitas
		C = np.arange(jumlah_chromo, dtype='f')
		total_x = 0
		for x in range(len(P)):
			total_x += P[x]
			C[x] = total_x

		#putar ROULETE WHELL sebnyak jumlah sel]
		R = np.random.sample(len(fitness))
		new_chrom = np.arange(jumlah_chromo*len(self.gen)).reshape(jumlah_chromo, len(self.gen))
		#CHROMOSOME BARU BERDASARKAN ROULETE WHELL
		for y in range(len(R)):
			for k in range(len(new_chrom)):
				if(R[y] < C[0]):
					new_chrom[y] = chrom[0]
				elif((C[k-1] < R[y]) & (R[y] < C[k])):
					new_chrom[y] = chrom[k]
					
		#CROSSOVER, mencari crossover
		R = np.random.sample(jumlah_chromo)
		index_chrom_parent = [] # [1,2,3, ...]
		for p in range(len(R)):
			if(R[p] < self.crossover_rate):
				index_chrom_parent.append(p)

		#MENENTUKAN POSISI CROSS OVER
		#membangkitkan bilangan acak dari 1 sampai (panjang chromosome - 1)
		posisi_CO = np.random.randint(low=1, high=len(self.gen), size=len(index_chrom_parent))

		#PROSES CROSSOVER, pertukaaran cut-point (?)
		off_spring = np.arange(len(self.gen)*len(index_chrom_parent)).reshape(len(index_chrom_parent), len(self.gen))

		for i_parent in range(len(index_chrom_parent)):
			index_chrome_1 = index_chrom_parent[i_parent]
			if(i_parent == len(index_chrom_parent)-1):
				index_chrome_2 = index_chrom_parent[0]
			else:
				index_chrome_2 = index_chrom_parent[i_parent+1]
			#melakukan cut-point
			cut_point = posisi_CO[i_parent]
			for p in range(len(new_chrom[index_chrome_1])):
				#LOOPING BERDASARKAN GEN
				if(p >= posisi_CO[i_parent]):
					#JIKA GEN[P] LEBIH BESAR ATAU SAMA DENGAN BILANGAN ACAK[P],
					#MAKA DIGANTI DGN CHROMOSOME KE-2
					off_spring[i_parent][p] = new_chrom[index_chrome_2][p]
				else:
					off_spring[i_parent][p] = new_chrom[index_chrome_1][p]

		#PROSES CROSSOVER DISIPMAN PADA VARIABLE 'OFF_SPRING'
		#MELAKUKAN PENGGABUNGAN OFF_SPTRING DENGAN NEW_CHROM
		for x in range(len(off_spring)):
			new_chrom[index_chrom_parent[x]] = off_spring[x]


		#PROSES MUTASI
		#Proses mutasi dilakukan dengan cara mengganti satu gen yang terpilih secara acak dengan suatu nilai baru yang didapat secara acak. Prosesnya adalah sebagai berikut. 
		#Pertama kita hitung dahulu panjang total gen yang ada dalam satu populasi. panjang total gen adalah total_gen     = (jumlah gen dalam chromosome) * jumlah populasi
		#= 4 * 6
		#= 24
		#Untuk memilih posisi gen yang mengalami mutasi dilakukan dengan cara membangkitkan bilangan integer acak antara 1 sampai total_gen, yaitu 1 sampai 24. 
		#Jika bilangan acak yang kita bangkitkan lebih kecil daripada variabel mutation_rate (ρm) maka pilih posisi tersebut sebagai sub-chromosome yang mengalami mutasi. 
		#Misal ρm kita tentukan 10% maka diharapkan ada 10% dari total_gen yang mengalami populasi:
		#jumlah mutasi      = 0.1 * 24
		#= 2.4
		#= 2
		
		total_gen = len(chrom) * len(chrom[0])
		jumlah_mutasi = self.mutasi_rate * total_gen
		jumlah_mutasi = int(jumlah_mutasi)

		random_i_mutasi = np.random.randint(low=0, high=total_gen, size=jumlah_mutasi)

		for x in range(len(random_i_mutasi)):
			index_mutasi = random_i_mutasi[x]
			banyak_kromosom = len(chrom)
			banyak_gen = len(chrom[0])
			random_value = random.randint(self.nilai_per_gen['min'], self.nilai_per_gen['max'])
			if(index_mutasi <= banyak_gen):
				#jika index_mutasi <= banyak gen, maka akan mengganti
				#gen pada chromosome baru yang ke-0
				new_chrom[0][index_mutasi-1]
			else:
				#POSISI Y DARI KROMOSOM, UNTUK MENCARI INDEX
				pos_y = index_mutasi/banyak_gen
				pos_y = int(pos_y)
				pos_x = index_mutasi % banyak_gen
				new_chrom[pos_y][pos_x] = random_value
		return new_chrom

	def do_now(self):
		chromosome_current = self.first_chromosome
		for generasi in range(0, self.total_generasi):
			if(self.stop != True):
				chromosome_current = self.evaluasi_chrom(chromosome_current, generasi)
		print("SELESAI !!")
		print("CHROMOSOME TERTINGGI ADALAH")
		print(self.next_gen)

run = Algoritma_genetika()
run.do_now()
