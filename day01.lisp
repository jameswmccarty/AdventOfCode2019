(defun counter-up (mass)
	(- 	(truncate (/ mass 3))
		2
	)
)

(defun counter-up-fuel (mass)
	(apply '+ 
		(loop while (<= 0 (counter-up mass)) collect (counter-up mass) 
			do (setq mass (counter-up mass))
		)
	)
)

(setq fuel 0)
(let ((in (open "./day01_input" :if-does-not-exist nil)))
   (when in
		(loop for line = (read-line in nil)
			while line do 
			(setq fuel
				(+	fuel
					(counter-up (parse-integer line)))
			)
		)	
		(close in)
	)
)
(print fuel)
(setq fuel 0)
(let ((in (open "./day01_input" :if-does-not-exist nil)))
   (when in
		(loop for line = (read-line in nil)
			while line do 
			(setq fuel
				(+	fuel
					(counter-up-fuel (parse-integer line)))
			)
		)	
		(close in)
	)
)
(print fuel)
