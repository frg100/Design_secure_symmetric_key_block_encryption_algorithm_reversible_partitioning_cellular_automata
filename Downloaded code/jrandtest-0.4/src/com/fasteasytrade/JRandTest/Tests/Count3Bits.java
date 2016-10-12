/*
 * Created on 03/02/2005
 *
 * JRandTest package
 *
 * Copyright (c) 2005, Zur Aougav, aougav@hotmail.com
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification, 
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice, this list 
 * of conditions and the following disclaimer. 
 * 
 * Redistributions in binary form must reproduce the above copyright notice, this 
 * list of conditions and the following disclaimer in the documentation and/or 
 * other materials provided with the distribution. 
 * 
 * Neither the name of the JRandTest nor the names of its contributors may be 
 * used to endorse or promote products derived from this software without specific 
 * prior written permission. 
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
 * ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package com.fasteasytrade.JRandTest.Tests;

/**
 * Count3Bits class extends Base
 * <p>
 * count 3 bits.
 * 
 * @author Zur Aougav 
 */

public class Count3Bits extends Base
{

	/**
	 * @see com.fasteasytrade.JRandTest.Tests.Base#help()
	 */
	public void help()
	{
		puts("\n\t|-------------------------------------------------------------|");
		puts("\t|    This is part of the Count test.  It counts consecutive   |");
		puts("\t|3 bits.                                                      |");
		puts("\t|-------------------------------------------------------------|\n");
	}

	/**
	 * @param filename input file with random data
	 */
	public void test(String filename) throws Exception
	{
		final int no_seqs = 8;
		double[] v1 = new double[no_seqs]; // count 3 bits - 000/001/010/../111
		long length = 0;

		printf("\t\t\tThe Count3Bits test for file " + filename + "\n");

		openInputStream();

		byte b, b2, b3;
		int temp;
		int i;

		while (true)
		{
			b = readByte();
			if (!isOpen())
				break;

			b2 = readByte();
			if (!isOpen())
				break;

			b3 = readByte();
			if (!isOpen())
				break;

			length += 8;

			/*
			 * temp has 24 bits of data. 
			 * loop and take 3 bits each time...
			 */
			temp = ((0xff & b) << 16) | ((0xff & b2) << 8) | (0xff & b3);

			for (i = 0; i < 8; i++)
			{

				v1[temp & 0x07]++; // increment counter for the first 3 bits
				temp = temp >>> 3; // delete the first 3 bits
			}
		}

		closeInputStream();

		double pv = KStest(v1, no_seqs);
		printf("\t ks test for " + no_seqs + " p's: " + d4(pv) + "\n");

		long k = length / v1.length;
		printf("\n\t found " + length + " 3 bits.");
		printf("\n\t expected avg for 3 bits: " + k);
		printf("\n\t found avg for 3 bits: " + d4(avg(v1)));
		for (int j = 0; j < no_seqs; j++)
			printf(
				"\n\t count 3 bits "
					+ j
					+ ": "
					+ d4((long) v1[j])
					+ "\tdelta: "
					+ d4(v1[j] - k)
					+ "\t%: "
					+ d4(100.00 * v1[j] / k - 100.00));

		double t = stdev(v1, k);
		printf("\n\t stdev for 3 bits\t: " + d4(t));
		printf("\n\t % stdev for 3 bits\t: %" + d4(100.00 * t / k));
		printf("\n\t chitest for 3 bits\t: " + d4(chitest(v1, k)));
		printf("\n\t r2 for 3 bits\t\t: " + d4(r2_double(v1)));

		return;
	}

} // end class
